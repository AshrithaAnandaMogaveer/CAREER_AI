import { useState } from 'react';
import { motion } from 'framer-motion';
import { Loader, CheckCircle } from 'lucide-react';
import Button from '../Button';
import { getAfter10thResult } from '../../services/postMatricsService';
import { validateAfter10thInput } from '../../utils/after10thScoring';

const After10th = () => {
  const [formData, setFormData] = useState({
    interests: [],
    strengthLevel: '',
    learningStyle: '',
  });
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState([]);

  const interestOptions = [
    'Logical/Math',
    'Science',
    'Business',
    'Creativity',
    'Communication',
    'Technology',
  ];

  const strengthLevels = ['Low', 'Medium', 'High'];

  const learningStyles = ['Practical', 'Theoretical', 'Creative'];

  const handleInterestToggle = (interest) => {
    setFormData((prev) => {
      const interests = prev.interests.includes(interest)
        ? prev.interests.filter((i) => i !== interest)
        : [...prev.interests, interest];
      return { ...prev, interests };
    });
    setErrors([]);
  };

  const handleStrengthChange = (level) => {
    setFormData((prev) => ({ ...prev, strengthLevel: level }));
    setErrors([]);
  };

  const handleLearningStyleChange = (style) => {
    setFormData((prev) => ({ ...prev, learningStyle: style }));
    setErrors([]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors([]);

    // Validate input
    const validation = validateAfter10thInput(formData);
    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    setIsLoading(true);

    try {
      const response = await getAfter10thResult(formData);
      
      if (response.success) {
        setResults(response.streams);
      } else {
        setErrors(['Failed to get recommendations. Please try again.']);
      }
    } catch (error) {
      setErrors([error.message || 'An error occurred. Please try again.']);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      interests: [],
      strengthLevel: '',
      learningStyle: '',
    });
    setResults(null);
    setErrors([]);
  };

  if (results) {
    return (
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h3 className="text-2xl font-semibold text-white">Your Recommended Streams</h3>
          <Button variant="secondary" onClick={handleReset}>
            Try Again
          </Button>
        </div>

        {/* Results */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {results.map((stream, index) => (
            <motion.div
              key={stream.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-[#161625] rounded-xl p-6 border border-gray-700 hover:border-[#00cccc] transition-all duration-200"
            >
              {/* Rank Badge */}
              <div className="flex items-center justify-between mb-4">
                <div className="w-10 h-10 rounded-full bg-[#00cccc] flex items-center justify-center">
                  <span className="text-black font-bold text-lg">#{index + 1}</span>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-white">{stream.score}%</div>
                  <div className="text-gray-400 text-xs">Match</div>
                </div>
              </div>

              {/* Stream Info */}
              <h4 className="text-xl font-semibold text-white mb-2">{stream.name}</h4>
              <p className="text-gray-400 text-sm mb-4">{stream.description}</p>

              {/* Reasoning */}
              <div className="mb-4 p-3 bg-[#0f0f1a] rounded-lg border border-gray-700">
                <p className="text-gray-300 text-sm">{stream.reasoning}</p>
              </div>

              {/* Career Options */}
              <div>
                <p className="text-gray-400 text-xs mb-2">Career Options:</p>
                <div className="flex flex-wrap gap-2">
                  {stream.careers.slice(0, 3).map((career, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-1 bg-[#00cccc]/10 border border-[#00cccc]/30 rounded-md text-[#00cccc] text-xs"
                    >
                      {career}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Additional Info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="bg-[#161625] rounded-xl p-6 border border-gray-700"
        >
          <h4 className="text-lg font-semibold text-white mb-3">Next Steps</h4>
          <ul className="space-y-2 text-gray-400 text-sm">
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-5 h-5 text-[#00cccc] flex-shrink-0 mt-0.5" />
              <span>Research the recommended streams in detail</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-5 h-5 text-[#00cccc] flex-shrink-0 mt-0.5" />
              <span>Talk to teachers and career counselors</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-5 h-5 text-[#00cccc] flex-shrink-0 mt-0.5" />
              <span>Explore career options in each stream</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-5 h-5 text-[#00cccc] flex-shrink-0 mt-0.5" />
              <span>Consider your long-term career goals</span>
            </li>
          </ul>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h3 className="text-2xl font-semibold text-white mb-2">After 10th Guidance</h3>
        <p className="text-gray-400">
          Answer a few questions to get personalized stream recommendations
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Interest Areas */}
        <div className="bg-[#161625] rounded-xl p-6 border border-gray-700">
          <label className="block text-white font-semibold mb-4">
            1. Select Your Interest Areas (Choose multiple)
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {interestOptions.map((interest) => (
              <button
                key={interest}
                type="button"
                onClick={() => handleInterestToggle(interest)}
                className={`p-3 rounded-md text-sm font-medium transition-all duration-200 ${
                  formData.interests.includes(interest)
                    ? 'bg-[#00cccc] text-black border border-[#00cccc]'
                    : 'bg-[#0f0f1a] text-white border border-gray-700 hover:border-[#00cccc]'
                }`}
              >
                {interest}
              </button>
            ))}
          </div>
        </div>

        {/* Strength Level */}
        <div className="bg-[#161625] rounded-xl p-6 border border-gray-700">
          <label className="block text-white font-semibold mb-4">
            2. How would you rate your overall academic strength?
          </label>
          <div className="grid grid-cols-3 gap-3">
            {strengthLevels.map((level) => (
              <button
                key={level}
                type="button"
                onClick={() => handleStrengthChange(level)}
                className={`p-4 rounded-md text-sm font-medium transition-all duration-200 ${
                  formData.strengthLevel === level
                    ? 'bg-[#00cccc] text-black border border-[#00cccc]'
                    : 'bg-[#0f0f1a] text-white border border-gray-700 hover:border-[#00cccc]'
                }`}
              >
                {level}
              </button>
            ))}
          </div>
        </div>

        {/* Learning Style */}
        <div className="bg-[#161625] rounded-xl p-6 border border-gray-700">
          <label className="block text-white font-semibold mb-4">
            3. What is your preferred learning style?
          </label>
          <div className="grid grid-cols-3 gap-3">
            {learningStyles.map((style) => (
              <button
                key={style}
                type="button"
                onClick={() => handleLearningStyleChange(style)}
                className={`p-4 rounded-md text-sm font-medium transition-all duration-200 ${
                  formData.learningStyle === style
                    ? 'bg-[#00cccc] text-black border border-[#00cccc]'
                    : 'bg-[#0f0f1a] text-white border border-gray-700 hover:border-[#00cccc]'
                }`}
              >
                {style}
              </button>
            ))}
          </div>
        </div>

        {/* Error Messages */}
        {errors.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-red-500/20 border border-red-500/50 rounded-lg p-4"
          >
            {errors.map((error, index) => (
              <p key={index} className="text-red-200 text-sm">
                • {error}
              </p>
            ))}
          </motion.div>
        )}

        {/* Submit Button */}
        <div className="flex justify-center">
          <Button
            type="submit"
            variant="primary"
            disabled={isLoading}
            className="px-12"
          >
            {isLoading ? (
              <span className="flex items-center space-x-2">
                <Loader className="animate-spin" size={18} />
                <span>Analyzing...</span>
              </span>
            ) : (
              'Get Recommendations'
            )}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default After10th;
