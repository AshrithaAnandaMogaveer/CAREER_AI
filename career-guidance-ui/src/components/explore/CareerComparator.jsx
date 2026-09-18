import { useState } from 'react';
import ExploreCard from './ExploreCard';
import ReasoningBox from './ReasoningBox';
import Toast from './Toast';

const CAREERS = [
  'Software Engineer', 'Data Scientist', 'Product Manager',
  'UX Designer', 'DevOps Engineer', 'Cybersecurity Analyst',
  'Machine Learning Engineer', 'Full Stack Developer',
];

const ROWS = [
  { key: 'salary',     label: 'Avg Salary' },
  { key: 'demand',     label: 'Market Demand' },
  { key: 'growth',     label: 'Growth Rate' },
  { key: 'time',       label: 'Time to Proficiency' },
  { key: 'difficulty', label: 'Difficulty' },
  { key: 'remote',     label: 'Remote Friendly' },
];

const CareerComparator = () => {
  const [careerA, setCareerA] = useState('');
  const [careerB, setCareerB] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [toast, setToast] = useState(null);

  const handleCompare = async () => {
    if (!careerA || !careerB) return;
    setLoading(true);
    setResult(null);
    setToast(null);
    try {
      const token = localStorage.getItem('authToken');
      const res = await fetch('http://localhost:5000/api/explore/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ careerA, careerB }),
      });
      const data = await res.json();
      if (data.success) setResult(data);
      else setToast({ message: data.message || 'Comparison failed.', type: 'error' });
    } catch {
      setToast({ message: 'Server unavailable. Please try again.', type: 'error', retry: true });
    } finally {
      setLoading(false);
    }
  };

  const dataA = result?.careerA || {};
  const dataB = result?.careerB || {};

  return (
    <ExploreCard
      icon="⚖️"
      title="Compare Careers"
      description="Side-by-side comparison of two career paths"
    >
      <div className="flex flex-col gap-3">
        <div className="grid grid-cols-2 gap-2">
          <select
            value={careerA}
            onChange={(e) => { setCareerA(e.target.value); setResult(null); }}
            className="bg-[#0f0f1a] border border-gray-700 text-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#00cccc]"
          >
            <option value="">Career A</option>
            {CAREERS.filter(c => c !== careerB).map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <select
            value={careerB}
            onChange={(e) => { setCareerB(e.target.value); setResult(null); }}
            className="bg-[#0f0f1a] border border-gray-700 text-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#00cccc]"
          >
            <option value="">Career B</option>
            {CAREERS.filter(c => c !== careerA).map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <button
          onClick={handleCompare}
          disabled={!careerA || !careerB || loading}
          className="w-full py-2 bg-[#00cccc] text-[#0f0f1a] font-semibold rounded-lg text-sm hover:bg-[#00aaaa] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading ? 'Comparing...' : 'Compare'}
        </button>

        {loading && (
          <div className="space-y-2 mt-1">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-4 bg-gray-700/50 rounded animate-pulse" />
            ))}
          </div>
        )}

        {!result && !loading && careerA && careerB && (
          <p className="text-gray-600 text-xs text-center">No data yet. Click Compare to see results.</p>
        )}

        {result && !loading && (
          <div className="mt-1 overflow-x-auto">
            {result.personalized && (
              <div className="flex gap-2 mb-3">
                <div className="flex-1 text-center bg-[#00cccc]/10 border border-[#00cccc]/20 rounded-lg py-1.5">
                  <p className="text-gray-500 text-xs">Your fit: {careerA}</p>
                  <p className="text-[#00cccc] font-bold text-sm">{result.careerA?.fit_score ?? '—'}%</p>
                </div>
                <div className="flex-1 text-center bg-purple-500/10 border border-purple-500/20 rounded-lg py-1.5">
                  <p className="text-gray-500 text-xs">Your fit: {careerB}</p>
                  <p className="text-purple-400 font-bold text-sm">{result.careerB?.fit_score ?? '—'}%</p>
                </div>
              </div>
            )}
            <table className="w-full text-sm">
              <thead>
                <tr>
                  <th className="text-left text-gray-500 font-medium pb-2 pr-3">Metric</th>
                  <th className="text-center text-[#00cccc] font-medium pb-2 px-2">{careerA}</th>
                  <th className="text-center text-purple-400 font-medium pb-2 pl-2">{careerB}</th>
                </tr>
              </thead>
              <tbody>
                {ROWS.map((row, i) => (
                  <tr key={row.key} className={i % 2 === 0 ? 'bg-[#0f0f1a]/50' : ''}>
                    <td className="text-gray-400 py-2 pr-3 rounded-l">{row.label}</td>
                    <td className="text-center text-white py-2 px-2">{dataA[row.key]}</td>
                    <td className="text-center text-white py-2 pl-2 rounded-r">{dataB[row.key]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <ReasoningBox reasoning={result.reasoning} />
          </div>
        )}
      </div>
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
          onRetry={toast.retry ? handleCompare : undefined}
        />
      )}
    </ExploreCard>
  );
};

export default CareerComparator;
