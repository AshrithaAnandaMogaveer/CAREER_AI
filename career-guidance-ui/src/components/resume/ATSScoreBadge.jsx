import { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertCircle, XCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { calculateATSScore, getScoreColor, getScoreGradient } from '../../utils/atsScorer';

const ATSScoreBadge = ({ resumeData }) => {
  const [showDetails, setShowDetails] = useState(false);

  // Memoize score calculation to prevent excessive re-computation
  const atsResult = useMemo(() => {
    return calculateATSScore(resumeData);
  }, [resumeData]);

  const { score, breakdown, recommendations } = atsResult;
  const { color, label } = getScoreColor(score);
  const gradient = getScoreGradient(score);

  // Calculate circle progress
  const circumference = 2 * Math.PI * 45; // radius = 45
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const ScoreIcon = score >= 76 ? CheckCircle : score >= 51 ? AlertCircle : XCircle;

  return (
    <div className="mb-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-xl p-6 glow-violet"
      >
        <div className="flex items-center justify-between">
          {/* Score Circle */}
          <div className="flex items-center space-x-4">
            <div className="relative">
              <svg width="100" height="100" className="transform -rotate-90">
                {/* Background circle */}
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  stroke="rgba(255, 255, 255, 0.1)"
                  strokeWidth="8"
                  fill="none"
                />
                {/* Progress circle */}
                <motion.circle
                  cx="50"
                  cy="50"
                  r="45"
                  stroke={color}
                  strokeWidth="8"
                  fill="none"
                  strokeLinecap="round"
                  initial={{ strokeDashoffset: circumference }}
                  animate={{ strokeDashoffset }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                  style={{
                    strokeDasharray: circumference,
                  }}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.5, type: 'spring' }}
                    className="text-2xl font-bold text-white"
                  >
                    {score}
                  </motion.div>
                  <div className="text-xs text-gray-400">/ 100</div>
                </div>
              </div>
            </div>

            <div>
              <div className="flex items-center space-x-2 mb-1">
                <h3 className="text-xl font-bold text-white">ATS Score</h3>
                <ScoreIcon className="w-5 h-5" style={{ color }} />
              </div>
              <p className="text-sm" style={{ color }}>{label}</p>
              <p className="text-xs text-gray-400 mt-1">
                Resume optimization score
              </p>
            </div>
          </div>

          {/* Toggle Details Button */}
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="flex items-center space-x-2 px-4 py-2 glass rounded-lg hover:glow-cyan transition-all duration-300"
          >
            <span className="text-sm text-white">
              {showDetails ? 'Hide' : 'Show'} Details
            </span>
            {showDetails ? (
              <ChevronUp className="w-4 h-4 text-gray-400" />
            ) : (
              <ChevronDown className="w-4 h-4 text-gray-400" />
            )}
          </button>
        </div>

        {/* Expandable Details */}
        {showDetails && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="mt-6 pt-6 border-t border-white/10"
          >
            {/* Score Breakdown */}
            <div className="mb-4">
              <h4 className="text-sm font-semibold text-white mb-3">Score Breakdown</h4>
              <div className="space-y-2">
                {Object.entries(breakdown).map(([key, value]) => (
                  <div key={key} className="flex items-center justify-between">
                    <span className="text-xs text-gray-400 capitalize">
                      {key.replace(/([A-Z])/g, ' $1').trim()}
                    </span>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 h-2 bg-white/10 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${(value / getMaxScore(key)) * 100}%` }}
                          transition={{ duration: 0.5 }}
                          className={`h-full bg-gradient-to-r ${gradient}`}
                        />
                      </div>
                      <span className="text-xs text-white font-medium w-8 text-right">
                        {value}/{getMaxScore(key)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendations */}
            {recommendations.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-white mb-3">Recommendations</h4>
                <ul className="space-y-2">
                  {recommendations.map((rec, index) => (
                    <motion.li
                      key={index}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="flex items-start space-x-2 text-xs text-gray-300"
                    >
                      <span className="text-cyan-400 mt-0.5">•</span>
                      <span>{rec}</span>
                    </motion.li>
                  ))}
                </ul>
              </div>
            )}
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};

// Helper function to get max score for each category
const getMaxScore = (category) => {
  const maxScores = {
    summary: 10,
    skills: 15,
    experience: 20,
    projects: 15,
    certifications: 10,
    contactInfo: 10,
    keywords: 20,
  };
  return maxScores[category] || 10;
};

export default ATSScoreBadge;
