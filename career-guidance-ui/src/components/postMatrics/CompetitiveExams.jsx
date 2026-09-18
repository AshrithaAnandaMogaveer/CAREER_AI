import { useState } from 'react';
import { motion } from 'framer-motion';
import { Trophy, Clock, Target } from 'lucide-react';
import Button from '../Button';

const CompetitiveExams = () => {
  const [formData, setFormData] = useState({
    educationLevel: '',
    timeAvailable: '',
    difficultyTolerance: '',
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const educationLevels = [
    { value: '10th', label: 'After 10th' },
    { value: '12th', label: 'After 12th' },
    { value: 'graduate', label: 'Graduate' },
    { value: 'postgraduate', label: 'Post Graduate' },
  ];

  const timeOptions = [
    { value: 'low', label: '< 6 months', multiplier: 0.7 },
    { value: 'medium', label: '6-12 months', multiplier: 1.0 },
    { value: 'high', label: '> 12 months', multiplier: 1.3 },
  ];

  const difficultyOptions = [
    { value: 'low', label: 'Low', multiplier: 1.2 },
    { value: 'medium', label: 'Medium', multiplier: 1.0 },
    { value: 'high', label: 'High', multiplier: 0.8 },
  ];

  const examDatabase = {
    '10th': [
      { name: 'NDA (National Defence Academy)', difficulty: 'medium', prepTime: 12, eligibility: '10th pass', benefits: 'Defence career' },
      { name: 'Sainik School Entrance', difficulty: 'low', prepTime: 6, eligibility: '10th appearing', benefits: 'Military education' },
    ],
    '12th': [
      { name: 'JEE Main', difficulty: 'high', prepTime: 18, eligibility: '12th PCM', benefits: 'Engineering admission' },
      { name: 'NEET', difficulty: 'high', prepTime: 18, eligibility: '12th PCB', benefits: 'Medical admission' },
      { name: 'CLAT', difficulty: 'medium', prepTime: 12, eligibility: '12th any stream', benefits: 'Law admission' },
      { name: 'NDA', difficulty: 'medium', prepTime: 12, eligibility: '12th pass', benefits: 'Defence career' },
    ],
    'graduate': [
      { name: 'UPSC CSE', difficulty: 'high', prepTime: 24, eligibility: 'Graduate', benefits: 'IAS/IPS/IFS' },
      { name: 'SSC CGL', difficulty: 'medium', prepTime: 12, eligibility: 'Graduate', benefits: 'Central govt jobs' },
      { name: 'Banking PO', difficulty: 'medium', prepTime: 9, eligibility: 'Graduate', benefits: 'Banking sector' },
      { name: 'CAT', difficulty: 'high', prepTime: 12, eligibility: 'Graduate', benefits: 'MBA admission' },
      { name: 'GATE', difficulty: 'high', prepTime: 12, eligibility: 'Engineering graduate', benefits: 'PSU/M.Tech' },
    ],
    'postgraduate': [
      { name: 'UGC NET', difficulty: 'high', prepTime: 12, eligibility: 'Post Graduate', benefits: 'Teaching/Research' },
      { name: 'UPSC CSE', difficulty: 'high', prepTime: 24, eligibility: 'Graduate', benefits: 'IAS/IPS/IFS' },
    ],
  };

  const calculateRecommendations = () => {
    setLoading(true);

    const exams = examDatabase[formData.educationLevel] || [];
    const timeMultiplier = timeOptions.find(t => t.value === formData.timeAvailable)?.multiplier || 1.0;
    const difficultyMultiplier = difficultyOptions.find(d => d.value === formData.difficultyTolerance)?.multiplier || 1.0;

    const scored = exams.map(exam => {
      let score = 50;

      const timeAvailableMonths = formData.timeAvailable === 'low' ? 6 : formData.timeAvailable === 'medium' ? 12 : 24;
      if (exam.prepTime <= timeAvailableMonths) {
        score += 20;
      } else {
        score += Math.max(0, 20 - ((exam.prepTime - timeAvailableMonths) / timeAvailableMonths) * 10);
      }

      const difficultyScores = { 'low': 15, 'medium': 20, 'high': 25 };
      if (exam.difficulty === formData.difficultyTolerance) {
        score += 25;
      } else {
        score += difficultyScores[exam.difficulty] || 15;
      }

      score *= timeMultiplier * difficultyMultiplier;

      return {
        ...exam,
        matchScore: Math.min(100, Math.round(score)),
      };
    });

    const sorted = scored.sort((a, b) => b.matchScore - a.matchScore).slice(0, 5);

    setTimeout(() => {
      setResults(sorted);
      setLoading(false);
    }, 1000);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    calculateRecommendations();
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'low': return 'text-green-400 bg-green-500/10 border-green-500/30';
      case 'medium': return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30';
      case 'high': return 'text-red-400 bg-red-500/10 border-red-500/30';
      default: return 'text-gray-400 bg-white/5 border-white/10';
    }
  };

  if (results) {
    return (
      <div className="space-y-6">
        <motion.h2 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-2xl font-semibold text-white mb-6"
        >
          Recommended Competitive Exams
        </motion.h2>
        
        {results.map((result, index) => (
          <motion.div 
            key={index} 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass rounded-lg p-6 glow-violet hover:glow-cyan transition-all duration-300"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <Trophy className="w-6 h-6 text-cyan-400" />
                  <h3 className="text-xl font-semibold text-white">{result.name}</h3>
                  <span className="px-3 py-1 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 border border-purple-500/30 rounded-full text-sm text-cyan-400">
                    Rank #{index + 1}
                  </span>
                </div>
              </div>
              <div className="ml-4 text-3xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
                {result.matchScore}%
              </div>
            </div>

            <div className="mb-4">
              <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: `${result.matchScore}%` }}
                  transition={{ duration: 1, delay: index * 0.1 + 0.3 }}
                  className="h-full bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className={`p-3 border rounded-lg backdrop-blur-sm ${getDifficultyColor(result.difficulty)}`}>
                <div className="flex items-center space-x-2 mb-1">
                  <Target className="w-4 h-4" />
                  <p className="text-xs font-medium">Difficulty</p>
                </div>
                <p className="text-sm font-semibold capitalize">{result.difficulty}</p>
              </div>
              <div className="p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg backdrop-blur-sm">
                <div className="flex items-center space-x-2 mb-1">
                  <Clock className="w-4 h-4 text-blue-400" />
                  <p className="text-xs text-gray-400">Prep Time</p>
                </div>
                <p className="text-sm font-semibold text-white">{result.prepTime} months</p>
              </div>
              <div className="p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg backdrop-blur-sm">
                <p className="text-xs text-gray-400 mb-1">Eligibility</p>
                <p className="text-sm font-semibold text-white">{result.eligibility}</p>
              </div>
            </div>

            <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg backdrop-blur-sm">
              <p className="text-xs text-gray-400 mb-1">Benefits</p>
              <p className="text-sm font-semibold text-green-400">{result.benefits}</p>
            </div>
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
      <motion.h2 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-2xl font-semibold text-white mb-6"
      >
        Find Your Competitive Exam
      </motion.h2>
      
      <motion.form 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        onSubmit={handleSubmit} 
        className="space-y-6"
      >
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Education Level
          </label>
          <select
            value={formData.educationLevel}
            onChange={(e) => setFormData({ ...formData, educationLevel: e.target.value })}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300"
            required
          >
            <option value="" className="bg-slate-800">Select education level</option>
            {educationLevels.map((level) => (
              <option key={level.value} value={level.value} className="bg-slate-800">
                {level.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Time Available for Preparation
          </label>
          <select
            value={formData.timeAvailable}
            onChange={(e) => setFormData({ ...formData, timeAvailable: e.target.value })}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300"
            required
          >
            <option value="" className="bg-slate-800">Select time available</option>
            {timeOptions.map((time) => (
              <option key={time.value} value={time.value} className="bg-slate-800">
                {time.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Difficulty Tolerance
          </label>
          <select
            value={formData.difficultyTolerance}
            onChange={(e) => setFormData({ ...formData, difficultyTolerance: e.target.value })}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300"
            required
          >
            <option value="" className="bg-slate-800">Select difficulty tolerance</option>
            {difficultyOptions.map((diff) => (
              <option key={diff.value} value={diff.value} className="bg-slate-800">
                {diff.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex justify-center pt-4">
          <Button type="submit" variant="primary" disabled={loading}>
            {loading ? 'Finding Exams...' : 'Find Exams'}
          </Button>
        </div>
      </motion.form>
    </div>
  );
};

export default CompetitiveExams;
