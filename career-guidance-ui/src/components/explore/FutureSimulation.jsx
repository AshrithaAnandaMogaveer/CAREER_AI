import { useState } from 'react';
import ExploreCard from './ExploreCard';
import ReasoningBox from './ReasoningBox';
import Toast from './Toast';

const CAREERS = [
  'Software Engineer', 'Data Scientist', 'Product Manager',
  'UX Designer', 'DevOps Engineer', 'Cybersecurity Analyst',
  'Machine Learning Engineer', 'Full Stack Developer',
];

const FutureSimulation = () => {
  const [career, setCareer] = useState('');
  const [duration, setDuration] = useState('6');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [toast, setToast] = useState(null);

  const handleGenerate = async () => {
    if (!career) return;
    setLoading(true);
    setResult(null);
    setToast(null);
    try {
      const token = localStorage.getItem('authToken');
      const res = await fetch('http://localhost:5000/api/explore/future', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ career, duration: parseInt(duration) }),
      });
      const data = await res.json();
      if (data.success) setResult(data);
      else setToast({ message: data.message || 'Failed to generate projection.', type: 'error' });
    } catch {
      setToast({ message: 'Server unavailable. Please try again.', type: 'error', retry: true });
    } finally {
      setLoading(false);
    }
  };

  return (
    <ExploreCard
      icon="🔮"
      title="Future Projection"
      description="See where you will be in 6–12 months"
    >
      <div className="flex flex-col gap-3">
        <select
          value={career}
          onChange={(e) => { setCareer(e.target.value); setResult(null); }}
          className="w-full bg-[#0f0f1a] border border-gray-700 text-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#00cccc]"
        >
          <option value="">Select Career Path</option>
          {CAREERS.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>

        <div className="flex gap-2">
          {['6', '12'].map((d) => (
            <button
              key={d}
              onClick={() => { setDuration(d); setResult(null); }}
              className={`flex-1 py-2 rounded-lg text-sm font-medium border transition-colors ${
                duration === d
                  ? 'bg-[#00cccc]/10 border-[#00cccc] text-[#00cccc]'
                  : 'border-gray-700 text-gray-400 hover:border-gray-500'
              }`}
            >
              {d} Months
            </button>
          ))}
        </div>

        <button
          onClick={handleGenerate}
          disabled={!career || loading}
          className="w-full py-2 bg-[#00cccc] text-[#0f0f1a] font-semibold rounded-lg text-sm hover:bg-[#00aaaa] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading ? 'Generating...' : 'Generate Projection'}
        </button>

        {loading && (
          <div className="space-y-2 mt-1">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-4 bg-gray-700/50 rounded animate-pulse" />
            ))}
          </div>
        )}

        {!result && !loading && career && (
          <p className="text-gray-600 text-xs text-center">No data yet. Click Generate to see your projection.</p>
        )}

        {result && !loading && (
          <div className="bg-[#0f0f1a] border border-gray-700 rounded-lg p-4 space-y-3 mt-1">
            {result.personalized && (
              <div className="flex items-center gap-1.5 mb-1">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00cccc]" />
                <span className="text-[#00cccc] text-xs">Based on your Analyze profile</span>
              </div>
            )}
            <div className="flex justify-between items-center">
              <span className="text-gray-400 text-sm">Expected Role</span>
              <span className="text-[#00cccc] font-medium text-sm">{result.expected_role}</span>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">Readiness Score</span>
                <span className="text-white">{result.future_readiness}%</span>
              </div>
              <div className="h-1.5 bg-gray-700 rounded-full">
                <div
                  className="h-1.5 bg-[#00cccc] rounded-full transition-all duration-700"
                  style={{ width: `${result.future_readiness}%` }}
                />
              </div>
            </div>
            <p className="text-gray-400 text-xs leading-relaxed">{result.message}</p>
            <ReasoningBox reasoning={result.reasoning} />
          </div>
        )}
      </div>
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
          onRetry={toast.retry ? handleGenerate : undefined}
        />
      )}
    </ExploreCard>
  );
};

export default FutureSimulation;