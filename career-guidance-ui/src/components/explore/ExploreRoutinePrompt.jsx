import { useState, useEffect } from 'react';

/**
 * Shows a "Build Routine" prompt when the user has missing skills.
 * Only renders if personalized summary has missing skills.
 */
const ExploreRoutinePrompt = ({ navigate }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    fetch('http://localhost:5000/api/explore/personalized-summary', {
      headers: { 'Authorization': `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((d) => { if (d.success && d.has_analysis) setData(d); })
      .catch(() => {});
  }, []);

  if (!data || !data.top_missing_skills || data.top_missing_skills.length === 0) return null;

  const topSkill = data.top_missing_skills[0];

  return (
    <div className="mb-8 bg-[#161625] border border-purple-500/20 rounded-xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <p className="text-purple-400 text-xs font-semibold tracking-widest uppercase mb-1">Skill Gap Detected</p>
        <p className="text-white font-semibold text-sm">
          Focus on <span className="text-[#00cccc]">{topSkill}</span> to improve your readiness
        </p>
        <p className="text-gray-400 text-xs mt-0.5">Build a structured learning routine to close this gap faster</p>
      </div>
      <button
        onClick={() => navigate('/routine-build')}
        className="flex-shrink-0 px-5 py-2.5 bg-purple-600 text-white font-semibold rounded-lg text-sm hover:bg-purple-500 transition-colors"
      >
        Build Routine →
      </button>
    </div>
  );
};

export default ExploreRoutinePrompt;
