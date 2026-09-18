import { useState } from 'react';
import { motion } from 'framer-motion';
import { Lightbulb } from 'lucide-react';
import Button from '../Button';

const After10thGuidance = () => {
  const [formData, setFormData] = useState({
    interests: [],
    strengthLevel: '',
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const interestOptions = [
    { value: 'science', label: 'Science & Technology', weight: { science: 10, commerce: 2, arts: 1 } },
    { value: 'mathematics', label: 'Mathematics', weight: { science: 10, commerce: 7, arts: 2 } },
    { value: 'business', label: 'Business & Commerce', weight: { science: 2, commerce: 10, arts: 3 } },
    { value: 'arts', label: 'Arts & Humanities', weight: { science: 1, commerce: 3, arts: 10 } },
    { value: 'social', label: 'Social Sciences', weight: { science: 2, commerce: 5, arts: 9 } },
  ];

  const strengthLevels = [
    { value: 'high', label: 'High', multiplier: 1.2 },
    { value: 'medium', label: 'Medium', multiplier: 1.0 },
    { value: 'low', label: 'Low', multiplier: 0.8 },
  ];

  const handleInterestToggle = (value) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(value)
        ? prev.interests.filter(i => i !== value)
        : [...prev.interests, value]
    }));
  };

  const calculateRecommendations = () => {
    setLoading(true);
    const scores = { science: 0, commerce: 0, arts: 0 };

    formData.interests.forEach(interest => {
      const option = interestOptions.find(opt => opt.value === interest);
      if (option) {
        scores.science += option.weight.science;
        scores.commerce += option.weight.commerce;
        scores.arts += option.weight.arts;
      }
    });

    const strengthMultiplier = strengthLevels.find(s => s.value === formData.strengthLevel)?.multiplier || 1.0;
    Object.keys(scores).forEach(key => {
      scores[key] *= strengthMultiplier;
    });

    const maxScore = Math.max(...Object.values(scores));
    const normalized = {};
    Object.keys(scores).forEach(key => {
      normalized[key] = maxScore > 0 ? Math.round((scores[key] / maxScore) * 100) : 0;
    });

    const streamDetails = {
      science: {
        name: 'Science (PCM/PCB)',
        description: 'Ideal for engineering, medicine, and research careers',
        careers: ['Engineering', 'Medicine', 'Research', 'Technology'],
        requirements: 'Strong foundation in Math and Science',
      },
      commerce: {
        name: 'Commerce',
        description: 'Perfect for business, finance, and management',
        careers: ['CA/CS', 'Banking', 'Business', 'Finance'],
        requirements: 'Good with numbers and business concepts',
      },
      arts: {
        name: 'Arts/Humanities',
        description: 'Great for social sciences and creative fields',
        careers: ['Law', 'Journalism', 'Psychology', 'Design'],
        requirements: 'Strong communication and analytical skills',
      },
    };

    const recommendations = Object.entries(normalized)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 3)
      .map(([stream, score]) => ({
        ...streamDetails[stream],
        score,
        reasoning: generateReasoning(stream, formData),
      }));

    setTimeout(() => {
      setResults(recommendations);
      setLoading(false);
    }, 1000);
  };

  const generateReasoning = (stream, data) => {
    const reasons = [];
    if (data.interests.includes('science') && stream === 'science') {
      reasons.push('Your interest in science aligns perfectly');
    }
    if (data.interests.includes('mathematics') && stream === 'science') {
      reasons.push('Strong mathematical interest supports this path');
    }
    if (data.interests.includes('business') && stream === 'commerce') {
      reasons.push('Your business inclination matches well');
    }
    if (data.interests.includes('arts') && stream === 'arts') {
      reasons.push('Your creative interests fit this stream');
    }
    return reasons.length > 0 ? reasons.join('. ') + '.' : 'This stream matches your profile.';
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    calculateRecommendations();
  };

  if (results) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-semibold text-white mb-6">Your Stream Recommendations</h2>
        
        {results.map((result, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="glass rounded-xl p-6 glow-violet"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="text-xl font-semibold text-white">{result.name}</h3>
                  <span className="px-3 py-1 glass rounded-full text-sm text-purple-300">
                    Rank #{index + 1}
                  </span>
                </div>
                <p className="text-gray-400 mb-2">{result.description}</p>
              </div>
              <div className="ml-4 text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                {result.score}%
              </div>
            </div>

            <div className="mb-4">
              <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: `${result.score}%` }}
                  transition={{ duration: 1, delay: 0.3 }}
                  className="h-full bg-gradient-to-r from-purple-500 to-blue-500 rounded-full"
                />
              </div>
            </div>

            <div className="mb-4 p-3 glass border border-purple-500/30 rounded-lg">
              <div className="flex items-start space-x-2">
                <Lightbulb className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-300">{result.reasoning}</p>
              </div>
            </div>

            <div className="mb-4">
              <p className="text-sm text-gray-400 mb-2">Career Opportunities:</p>
              <div className="flex flex-wrap gap-2">
                {result.careers.map((career, idx) => (
                  <span key={idx} className="px-3 py-1 glass rounded-full text-xs text-gray-300">
                    {career}
                  </span>
                ))}
              </div>
            </div>

            <p className="text-sm text-gray-400">
              <strong className="text-gray-300">Requirements:</strong> {result.requirements}
            </p>
          </motion.div>
        ))}

        <div className="text-center">
          <Button variant="secondary" onClick={() => setResults(null)}>
            Try Again
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-white mb-6">After 10th Stream Selection</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-3">
            Select Your Interests (Multiple)
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {interestOptions.map((option) => (
              <motion.button
                key={option.value}
                type="button"
                onClick={() => handleInterestToggle(option.value)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`p-3 rounded-lg text-sm transition-all duration-300 ${
                  formData.interests.includes(option.value)
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white glow-violet'
                    : 'glass text-gray-300 hover:glow-violet'
                }`}
              >
                {option.label}
              </motion.button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Your Academic Strength Level
          </label>
          <select
            value={formData.strengthLevel}
            onChange={(e) => setFormData({ ...formData, strengthLevel: e.target.value })}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 transition-all duration-300"
            required
          >
            <option value="" className="bg-slate-800">Select strength level</option>
            {strengthLevels.map((level) => (
              <option key={level.value} value={level.value} className="bg-slate-800">
                {level.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex justify-center pt-4">
          <Button
            type="submit"
            variant="primary"
            disabled={loading || formData.interests.length === 0}
          >
            {loading ? 'Analyzing...' : 'Get Recommendations'}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default After10thGuidance;
