import { useState } from 'react';
import ExploreCard from './ExploreCard';
import ReasoningBox from './ReasoningBox';
import Toast from './Toast';

const SKILLS = [
  'React', 'Python', 'Machine Learning', 'AWS', 'Docker',
  'TypeScript', 'SQL', 'Kubernetes', 'System Design', 'Data Analysis',
];

const ROI_COLOR = { 'Very High': 'text-emerald-400', 'High': 'text-[#00cccc]', 'Medium': 'text-yellow-400', 'Low': 'text-red-400' };
const EFFORT_COLOR = { 'Low': 'text-emerald-400', 'Medium': 'text-yellow-400', 'High': 'text-red-400' };

const Bar = ({ value, color }) => (
  <div className="h-1.5 bg-gray-700 rounded-full mt-1">
    <div className={`h-1.5 rounded-full transition-all duration-700 ${color}`} style={{ width: `${value}%` }} />
  </div>
);

const SkillROI = () => {
  const [skill, setSkill] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [toast, setToast] = useState(null);

  const handleAnalyze = async () => {
    if (!skill) return;
    setLoading(true);
    setResult(null);
    setToast(null);
    try {
      const token = localStorage.getItem('authToken');
      const res = await fetch('http://localhost:5000/api/explore/roi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ skill }),
      });
      const data = await res.json();
      if (data.success) setResult(data);
      else setToast({ message: data.message || 'Analysis failed.', type: 'error' });
    } catch {
      setToast({ message: 'Server unavailable. Please try again.', type: 'error', retry: true });
    } finally {
      setLoading(false);
    }
  };

  return (
    <ExploreCard
      icon="📈"
      title="Skill ROI Analyzer"
      description="Understand the return on investment for learning a skill"
    >
      <div className="flex flex-col gap-3">
        <select
          value={skill}
          onChange={(e) => { setSkill(e.target.value); setResult(null); }}
          className="w-full bg-[#0f0f1a] border border-gray-700 text-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#00cccc]"
        >
          <option value="">Select a Skill</option>
          {SKILLS.map(s => <option key={s} value={s}>{s}</option>)}
        </select>

        <button
          onClick={handleAnalyze}
          disabled={!skill || loading}
          className="w-full py-2 bg-[#00cccc] text-[#0f0f1a] font-semibold rounded-lg text-sm hover:bg-[#00aaaa] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading ? 'Analyzing...' : 'Analyze ROI'}
        </button>

        {loading && (
          <div className="space-y-2 mt-1">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-4 bg-gray-700/50 rounded animate-pulse" />
            ))}
          </div>
        )}

        {!result && !loading && skill && (
          <p className="text-gray-600 text-xs text-center">No data yet. Click Analyze ROI to see results.</p>
        )}

        {result && !loading && (
          <div className="bg-[#0f0f1a] border border-gray-700 rounded-lg p-4 space-y-3 mt-1">
            {result.high_priority && (
              <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/20 rounded-lg px-3 py-2">
                <span className="text-red-400 text-xs font-semibold">⚠ High-ROI skill you're missing — prioritize this</span>
              </div>
            )}
            {result.you_have_this_skill && (
              <div className="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 rounded-lg px-3 py-2">
                <span className="text-emerald-400 text-xs font-semibold">✓ You already have this skill</span>
              </div>
            )}
            <div className="grid grid-cols-3 gap-2 text-center">
              <div className="bg-[#161625] rounded-lg p-2">
                <p className="text-gray-500 text-xs mb-1">ROI</p>
                <p className={`font-semibold text-sm ${ROI_COLOR[result.roi]}`}>{result.roi}</p>
              </div>
              <div className="bg-[#161625] rounded-lg p-2">
                <p className="text-gray-500 text-xs mb-1">Salary Boost</p>
                <p className="text-white font-semibold text-xs">{result.salary_boost}</p>
              </div>
              <div className="bg-[#161625] rounded-lg p-2">
                <p className="text-gray-500 text-xs mb-1">Effort</p>
                <p className={`font-semibold text-sm ${EFFORT_COLOR[result.effort]}`}>{result.effort}</p>
              </div>
            </div>

            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Time to Learn</span>
              <span className="text-white">{result.time_to_learn}</span>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-0.5">
                <span className="text-gray-400">Market Demand</span>
                <span className="text-white">{result.demand}%</span>
              </div>
              <Bar value={result.demand} color="bg-[#00cccc]" />
            </div>

            <div>
              <div className="flex justify-between text-xs mb-0.5">
                <span className="text-gray-400">Career Impact</span>
                <span className="text-white">{result.impact_score}%</span>
              </div>
              <Bar value={result.impact_score} color="bg-purple-500" />
            </div>

            {result.missing_high_roi && result.missing_high_roi.length > 0 && (
              <div className="border-t border-gray-700/60 pt-3">
                <p className="text-gray-500 text-xs mb-1.5">Other high-ROI skills you're missing:</p>
                <div className="flex flex-wrap gap-1">
                  {result.missing_high_roi.map((s) => (
                    <span key={s} className="px-2 py-0.5 bg-[#00cccc]/10 text-[#00cccc] text-xs rounded-full border border-[#00cccc]/20">{s}</span>
                  ))}
                </div>
              </div>
            )}
            <ReasoningBox reasoning={result.reasoning} />
          </div>
        )}
      </div>
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
          onRetry={toast.retry ? handleAnalyze : undefined}
        />
      )}
    </ExploreCard>
  );
};

export default SkillROI;
