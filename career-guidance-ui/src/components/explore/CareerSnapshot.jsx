import { useState, useEffect } from 'react';

const CareerSnapshot = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(false);

  const fetchSnapshot = () => {
    setLoading(true);
    setFetchError(false);
    const token = localStorage.getItem('authToken');
    fetch('http://localhost:5000/api/explore/personalized-summary', {
      headers: { 'Authorization': `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((d) => { if (d.success) setData(d); })
      .catch(() => setFetchError(true))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchSnapshot(); }, []);

  // Don't render if no analysis data exists yet
  if (loading) {
    return (
      <div className="mb-10 bg-[#161625] border border-gray-700/60 rounded-xl p-5 animate-pulse">
        <div className="h-4 bg-gray-700/50 rounded w-1/3 mb-4" />
        <div className="grid grid-cols-3 gap-4">
          {[...Array(3)].map((_, i) => <div key={i} className="h-16 bg-gray-700/40 rounded-lg" />)}
        </div>
      </div>
    );
  }

  if (!data || !data.has_analysis) {
    if (fetchError) {
      return (
        <div className="mb-10 bg-[#161625] border border-dashed border-red-700/40 rounded-xl p-5 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-2xl">⚠️</span>
            <p className="text-red-400 text-sm">Could not load your career snapshot.</p>
          </div>
          <button
            onClick={fetchSnapshot}
            className="text-xs text-[#00cccc] border border-[#00cccc]/30 px-3 py-1.5 rounded-lg hover:bg-[#00cccc]/10 transition-colors"
          >
            Retry
          </button>
        </div>
      );
    }
    return null;
  }

  const readiness = data.current_level || 0;
  const readinessColor = readiness >= 70 ? 'text-emerald-400' : readiness >= 45 ? 'text-yellow-400' : 'text-red-400';
  const barColor = readiness >= 70 ? 'bg-emerald-400' : readiness >= 45 ? 'bg-yellow-400' : 'bg-red-400';

  return (
    <div className="mb-10 bg-[#161625] border border-[#00cccc]/20 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-[#00cccc] text-xs font-semibold tracking-widest uppercase">Your Career Snapshot</span>
        <span className="text-xs bg-[#00cccc]/10 text-[#00cccc] border border-[#00cccc]/20 px-2 py-0.5 rounded-full">Personalized</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Readiness */}
        <div className="bg-[#0f0f1a] rounded-lg p-4">
          <p className="text-gray-500 text-xs mb-1">Current Readiness</p>
          <p className={`text-2xl font-bold ${readinessColor}`}>{readiness}%</p>
          <div className="h-1.5 bg-gray-700 rounded-full mt-2">
            <div className={`h-1.5 rounded-full transition-all duration-700 ${barColor}`} style={{ width: `${readiness}%` }} />
          </div>
        </div>

        {/* Target Role */}
        <div className="bg-[#0f0f1a] rounded-lg p-4">
          <p className="text-gray-500 text-xs mb-1">Target Role</p>
          <p className="text-white font-semibold text-sm leading-snug">{data.target_role || 'Not set'}</p>
          {data.recommended_focus && (
            <p className="text-[#00cccc] text-xs mt-1.5">Focus: {data.recommended_focus}</p>
          )}
        </div>

        {/* Missing Skills */}
        <div className="bg-[#0f0f1a] rounded-lg p-4">
          <p className="text-gray-500 text-xs mb-2">Key Skills to Gain</p>
          {data.top_missing_skills && data.top_missing_skills.length > 0 ? (
            <div className="flex flex-wrap gap-1">
              {data.top_missing_skills.slice(0, 4).map((s) => (
                <span key={s} className="px-2 py-0.5 bg-red-500/10 text-red-400 text-xs rounded-full border border-red-500/20">
                  {s}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-gray-400 text-xs">No gaps detected</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default CareerSnapshot;
