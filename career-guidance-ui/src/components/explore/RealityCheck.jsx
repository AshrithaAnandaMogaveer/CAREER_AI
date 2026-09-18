import { useState } from 'react';
import ExploreCard from './ExploreCard';
import ReasoningBox from './ReasoningBox';
import Toast from './Toast';

const CAREERS = [
  'Software Engineer', 'Data Scientist', 'Product Manager',
  'UX Designer', 'DevOps Engineer', 'Cybersecurity Analyst',
  'Machine Learning Engineer', 'Full Stack Developer',
];

const LEVEL_COLOR = {
  'Low': 'text-emerald-400', 'Medium': 'text-yellow-400',
  'High': 'text-orange-400', 'Very High': 'text-red-400',
};

const ScoreBar = ({ label, value, color }) => (
  <div>
    <div className="flex justify-between text-xs mb-1">
      <span className="text-gray-400">{label}</span>
      <span className="text-white">{value}%</span>
    </div>
    <div className="h-1.5 bg-gray-700 rounded-full">
      <div className={`h-1.5 rounded-full transition-all duration-700 ${color}`} style={{ width: `${value}%` }} />
    </div>
  </div>
);

const RealityCheck = () => {
  const [career, setCareer] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [toast, setToast] = useState(null);

  const handleCheck = async () => {
    if (!career) return;
    setLoading(true);
    setResult(null);
    setToast(null);
    try {
      const token = localStorage.getItem('authToken');
      const res = await fetch(
        `http://localhost:5000/api/explore/reality?career=${encodeURIComponent(career)}`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      const data = await res.json();
      if (data.success) setResult(data);
      else setToast({ message: data.message || 'Failed to load reality check.', type: 'error' });
    } catch {
      setToast({ message: 'Server unavailable. Please try again.', type: 'error', retry: true });
    } finally {
      setLoading(false);
    }
  };

  return (
    <ExploreCard
      icon="🎯"
      title="Reality Check"
      description="Get an honest assessment of what a career path actually demands"
    >
      <div className="flex flex-col gap-3">
        <select
          value={career}
          onChange={(e) => { setCareer(e.target.value); setResult(null); }}
          className="w-full bg-[#0f0f1a] border border-gray-700 text-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#00cccc]"
        >
          <option value="">Select a Career</option>
          {CAREERS.map(c => <option key={c} value={c}>{c}</option>)}
        </select>

        <button
          onClick={handleCheck}
          disabled={!career || loading}
          className="w-full py-2 bg-[#00cccc] text-[#0f0f1a] font-semibold rounded-lg text-sm hover:bg-[#00aaaa] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading ? 'Checking...' : 'Reality Check'}
        </button>

        {loading && (
          <div className="space-y-2 mt-1">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-4 bg-gray-700/50 rounded animate-pulse" />
            ))}
          </div>
        )}

        {!result && !loading && career && (
          <p className="text-gray-600 text-xs text-center">No data yet. Click Reality Check to see results.</p>
        )}

        {result && !loading && (
          <div className="bg-[#0f0f1a] border border-gray-700 rounded-lg p-4 space-y-3 mt-1">
            <div className="grid grid-cols-2 gap-2">
              {[
                { label: 'Difficulty',    value: result.difficulty },
                { label: 'Time Required', value: result.learning_time },
                { label: 'Competition',   value: result.competition },
                { label: 'Effort',        value: result.effort },
              ].map(item => (
                <div key={item.label} className="bg-[#161625] rounded-lg p-2.5">
                  <p className="text-gray-500 text-xs mb-0.5">{item.label}</p>
                  <p className={`font-semibold text-sm ${LEVEL_COLOR[item.value] || 'text-white'}`}>
                    {item.value}
                  </p>
                </div>
              ))}
            </div>

            <ScoreBar label="Difficulty Level"  value={result.diff_score}   color="bg-orange-400" />
            <ScoreBar label="Competition Level" value={result.comp_score}   color="bg-red-400" />
            <ScoreBar label="Effort Required"   value={result.effort_score} color="bg-purple-500" />

            {result.personalized && result.your_readiness > 0 && (
              <div className="bg-[#161625] rounded-lg p-3 flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-xs">Your current readiness</p>
                  <p className={`font-bold text-sm ${result.your_readiness >= 70 ? 'text-emerald-400' : result.your_readiness >= 45 ? 'text-yellow-400' : 'text-red-400'}`}>
                    {result.your_readiness}%
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-gray-500 text-xs">Gap to close</p>
                  <p className="text-white font-semibold text-sm">{result.readiness_gap}%</p>
                </div>
              </div>
            )}

            <div className="border-t border-gray-700/60 pt-3">
              <p className="text-gray-500 text-xs mb-1">Honest Verdict</p>
              <p className="text-gray-300 text-xs leading-relaxed">{result.verdict}</p>
            </div>
            <ReasoningBox reasoning={result.reasoning} />
          </div>
        )}
      </div>
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
          onRetry={toast.retry ? handleCheck : undefined}
        />
      )}
    </ExploreCard>
  );
};

export default RealityCheck;
