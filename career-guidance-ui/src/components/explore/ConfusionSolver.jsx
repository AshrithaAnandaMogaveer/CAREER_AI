import { useState } from 'react';
import ExploreCard from './ExploreCard';
import Toast from './Toast';

const QUESTIONS = [
  {
    id: 'interest',
    label: 'What type of work interests you most?',
    options: ['Building products', 'Analyzing data', 'Designing experiences', 'Securing systems', 'Managing teams'],
  },
  {
    id: 'workStyle',
    label: 'How do you prefer to work?',
    options: ['Solo deep work', 'Collaborative teams', 'Mix of both', 'Client-facing', 'Remote independent'],
  },
  {
    id: 'math',
    label: 'How comfortable are you with math/statistics?',
    options: ['Very comfortable', 'Somewhat comfortable', 'Neutral', 'Prefer to avoid', 'Not at all'],
  },
  {
    id: 'creativity',
    label: 'How important is creativity in your work?',
    options: ['Essential', 'Important', 'Moderate', 'Minor', 'Not important'],
  },
  {
    id: 'risk',
    label: 'What is your risk tolerance?',
    options: ['High – love uncertainty', 'Medium – calculated risks', 'Low – prefer stability', 'Very low – need security'],
  },
];

const ConfusionSolver = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [answers, setAnswers] = useState({});
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [toast, setToast] = useState(null);

  const handleAnswer = (questionId, value) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setToast(null);
    try {
      const token = localStorage.getItem('authToken');
      // Map question answers to API fields
      const interestMap = {
        'Building products': 'building', 'Analyzing data': 'analytical',
        'Designing experiences': 'design', 'Securing systems': 'security', 'Managing teams': 'management',
      };
      const mathMap = {
        'Very comfortable': 'high', 'Somewhat comfortable': 'medium',
        'Neutral': 'medium', 'Prefer to avoid': 'low', 'Not at all': 'low',
      };
      const creativityMap = {
        'Essential': 'high', 'Important': 'high', 'Moderate': 'medium', 'Minor': 'low', 'Not important': 'low',
      };
      const riskMap = {
        'High – love uncertainty': 'high', 'Medium – calculated risks': 'medium',
        'Low – prefer stability': 'low', 'Very low – need security': 'low',
      };

      const res = await fetch('http://localhost:5000/api/explore/path-suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({
          interest: interestMap[answers.interest] || answers.interest,
          math_level: mathMap[answers.math] || answers.math,
          creativity: creativityMap[answers.creativity] || answers.creativity,
          risk: riskMap[answers.risk] || answers.risk,
        }),
      });
      const data = await res.json();
      if (data.success) {
        setResult({
          career: data.suggested_careers[0],
          careers: data.suggested_careers,
          match: data.match_score,
          why: data.why,
          next: data.next_steps,
        });
      } else {
        setToast({ message: 'Could not determine path. Please try again.', type: 'error' });
      }
    } catch {
      setToast({ message: 'Server unavailable. Please try again.', type: 'error', retry: true });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAnswers({});
    setStep(0);
    setResult(null);
    setIsOpen(false);
  };

  const allAnswered = QUESTIONS.every(q => answers[q.id]);
  const currentQ = QUESTIONS[step];

  return (
    <ExploreCard
      icon="🧭"
      title="Find Your Path"
      description="Answer 5 questions to discover your ideal career direction"
    >
      <div className="flex flex-col gap-3">
        {!isOpen && !result && (
          <button
            onClick={() => setIsOpen(true)}
            className="w-full py-2.5 bg-[#00cccc] text-[#0f0f1a] font-semibold rounded-lg text-sm hover:bg-[#00aaaa] transition-colors"
          >
            Start Assessment
          </button>
        )}

        {isOpen && !result && (
          <div className="space-y-4">
            {/* Progress */}
            <div className="flex items-center gap-2">
              <div className="flex-1 h-1 bg-gray-700 rounded-full">
                <div
                  className="h-1 bg-[#00cccc] rounded-full transition-all duration-300"
                  style={{ width: `${((step + 1) / QUESTIONS.length) * 100}%` }}
                />
              </div>
              <span className="text-gray-500 text-xs">{step + 1}/{QUESTIONS.length}</span>
            </div>

            {/* Current Question */}
            <div>
              <p className="text-white text-sm font-medium mb-2">{currentQ.label}</p>
              <div className="space-y-1.5">
                {currentQ.options.map(opt => (
                  <button
                    key={opt}
                    onClick={() => handleAnswer(currentQ.id, opt)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm border transition-colors ${
                      answers[currentQ.id] === opt
                        ? 'border-[#00cccc] bg-[#00cccc]/10 text-[#00cccc]'
                        : 'border-gray-700 text-gray-400 hover:border-gray-500 hover:text-gray-300'
                    }`}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>

            {/* Navigation */}
            <div className="flex gap-2">
              {step > 0 && (
                <button
                  onClick={() => setStep(s => s - 1)}
                  className="flex-1 py-2 border border-gray-700 text-gray-400 rounded-lg text-sm hover:border-gray-500 transition-colors"
                >
                  Back
                </button>
              )}
              {step < QUESTIONS.length - 1 ? (
                <button
                  onClick={() => setStep(s => s + 1)}
                  disabled={!answers[currentQ.id]}
                  className="flex-1 py-2 bg-[#161625] border border-gray-700 text-gray-300 rounded-lg text-sm hover:border-[#00cccc] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              ) : (
                <button
                  onClick={handleSubmit}
                  disabled={!allAnswered || loading}
                  className="flex-1 py-2 bg-[#00cccc] text-[#0f0f1a] font-semibold rounded-lg text-sm hover:bg-[#00aaaa] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  {loading ? 'Analyzing...' : 'Get My Path'}
                </button>
              )}
            </div>

            <button
              onClick={handleReset}
              className="text-gray-600 text-xs hover:text-gray-400 transition-colors text-center w-full"
            >
              Cancel
            </button>
          </div>
        )}

        {loading && (
          <div className="space-y-2">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-4 bg-gray-700/50 rounded animate-pulse" />
            ))}
          </div>
        )}

        {result && !loading && (
          <div className="bg-[#0f0f1a] border border-gray-700 rounded-lg p-4 space-y-3">
            <div className="flex items-center justify-between">
              <p className="text-[#00cccc] font-semibold text-sm">{result.career}</p>
              <span className="text-xs bg-[#00cccc]/10 text-[#00cccc] border border-[#00cccc]/20 px-2 py-0.5 rounded-full">
                {result.match}% match
              </span>
            </div>
            {result.careers && result.careers.length > 1 && (
              <div className="flex flex-wrap gap-1">
                {result.careers.slice(1).map((c) => (
                  <span key={c} className="px-2 py-0.5 bg-gray-700/50 text-gray-300 text-xs rounded-full">{c}</span>
                ))}
              </div>
            )}
            <p className="text-gray-400 text-xs leading-relaxed">{result.why}</p>
            {result.next && result.next.length > 0 && (
              <div>
                <p className="text-gray-500 text-xs mb-1.5">Recommended next steps:</p>
                <ul className="space-y-1">
                  {result.next.map((s, i) => (
                    <li key={i} className="flex items-center gap-2 text-xs text-gray-300">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#00cccc] flex-shrink-0" />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            <button
              onClick={handleReset}
              className="text-gray-500 text-xs hover:text-gray-300 transition-colors"
            >
              Retake Assessment
            </button>
          </div>
        )}
      </div>
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
          onRetry={toast.retry ? handleSubmit : undefined}
        />
      )}
    </ExploreCard>
  );
};

export default ConfusionSolver;
