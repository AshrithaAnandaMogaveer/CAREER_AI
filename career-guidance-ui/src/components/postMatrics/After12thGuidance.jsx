import { useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp } from 'lucide-react';
import Button from '../Button';

const After12thGuidance = () => {
  const [formData, setFormData] = useState({
    stream: '',
    budget: '',
    preference: '',
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const streams = [
    { value: 'pcm', label: 'PCM (Physics, Chemistry, Math)' },
    { value: 'pcb', label: 'PCB (Physics, Chemistry, Biology)' },
    { value: 'commerce', label: 'Commerce' },
    { value: 'arts', label: 'Arts/Humanities' },
  ];

  const budgets = [
    { value: 'low', label: 'Low (< ₹2L/year)', multiplier: 1.0 },
    { value: 'medium', label: 'Medium (₹2-5L/year)', multiplier: 1.2 },
    { value: 'high', label: 'High (> ₹5L/year)', multiplier: 1.5 },
  ];

  const preferences = [
    { value: 'technical', label: 'Technical/Engineering' },
    { value: 'government', label: 'Government Jobs' },
    { value: 'business', label: 'Business/Entrepreneurship' },
    { value: 'creative', label: 'Creative/Design' },
  ];

  const careerDatabase = {
    pcm: {
      technical: [
        { name: 'B.Tech/B.E.', duration: '4 years', avgCost: 400000, roi: 9, demand: 'Very High' },
        { name: 'B.Sc. Computer Science', duration: '3 years', avgCost: 150000, roi: 8, demand: 'High' },
        { name: 'B.Arch', duration: '5 years', avgCost: 500000, roi: 7, demand: 'Medium' },
      ],
      government: [
        { name: 'NDA/CDS', duration: '4 years', avgCost: 0, roi: 8, demand: 'High' },
        { name: 'B.Sc. + SSC/Banking', duration: '3 years', avgCost: 100000, roi: 7, demand: 'High' },
      ],
      business: [
        { name: 'BBA', duration: '3 years', avgCost: 300000, roi: 6, demand: 'Medium' },
      ],
      creative: [
        { name: 'B.Des', duration: '4 years', avgCost: 600000, roi: 6, demand: 'Medium' },
      ],
    },
    pcb: {
      technical: [
        { name: 'MBBS', duration: '5.5 years', avgCost: 5000000, roi: 10, demand: 'Very High' },
        { name: 'B.Pharm', duration: '4 years', avgCost: 400000, roi: 7, demand: 'High' },
        { name: 'BDS', duration: '5 years', avgCost: 3000000, roi: 8, demand: 'High' },
      ],
      government: [
        { name: 'B.Sc. Nursing + Govt Jobs', duration: '4 years', avgCost: 200000, roi: 7, demand: 'High' },
      ],
      business: [
        { name: 'B.Sc. + MBA Healthcare', duration: '3 years', avgCost: 250000, roi: 6, demand: 'Medium' },
      ],
      creative: [
        { name: 'B.Sc. Biotechnology', duration: '3 years', avgCost: 300000, roi: 6, demand: 'Medium' },
      ],
    },
    commerce: {
      technical: [
        { name: 'B.Com + CA', duration: '3 years', avgCost: 200000, roi: 9, demand: 'Very High' },
        { name: 'BBA (IT)', duration: '3 years', avgCost: 350000, roi: 7, demand: 'High' },
      ],
      government: [
        { name: 'B.Com + Banking/SSC', duration: '3 years', avgCost: 100000, roi: 8, demand: 'Very High' },
      ],
      business: [
        { name: 'BBA + MBA', duration: '3 years', avgCost: 400000, roi: 8, demand: 'High' },
        { name: 'B.Com + CS', duration: '3 years', avgCost: 150000, roi: 8, demand: 'High' },
      ],
      creative: [
        { name: 'B.Des (Fashion/Product)', duration: '4 years', avgCost: 500000, roi: 6, demand: 'Medium' },
      ],
    },
    arts: {
      technical: [
        { name: 'BA + Web Development', duration: '3 years', avgCost: 150000, roi: 7, demand: 'High' },
      ],
      government: [
        { name: 'BA + UPSC/State PSC', duration: '3 years', avgCost: 100000, roi: 9, demand: 'High' },
        { name: 'LLB', duration: '5 years', avgCost: 300000, roi: 8, demand: 'High' },
      ],
      business: [
        { name: 'BA + MBA', duration: '3 years', avgCost: 250000, roi: 7, demand: 'Medium' },
      ],
      creative: [
        { name: 'BA Journalism', duration: '3 years', avgCost: 200000, roi: 6, demand: 'Medium' },
        { name: 'BA Psychology', duration: '3 years', avgCost: 150000, roi: 7, demand: 'High' },
        { name: 'BA Fine Arts', duration: '3 years', avgCost: 250000, roi: 5, demand: 'Low' },
      ],
    },
  };

  const calculateRecommendations = () => {
    setLoading(true);

    const careers = careerDatabase[formData.stream]?.[formData.preference] || [];
    const budgetMultiplier = budgets.find(b => b.value === formData.budget)?.multiplier || 1.0;

    const scored = careers.map(career => {
      let feasibilityScore = 0;

      const budgetValue = formData.budget === 'low' ? 200000 : formData.budget === 'medium' ? 500000 : 10000000;
      if (career.avgCost <= budgetValue) {
        feasibilityScore += 30;
      } else {
        feasibilityScore += Math.max(0, 30 - ((career.avgCost - budgetValue) / budgetValue) * 20);
      }

      feasibilityScore += career.roi * 3;

      const demandScores = { 'Very High': 25, 'High': 20, 'Medium': 15, 'Low': 10 };
      feasibilityScore += demandScores[career.demand] || 10;

      feasibilityScore *= budgetMultiplier;

      return {
        ...career,
        feasibilityScore: Math.min(100, Math.round(feasibilityScore)),
      };
    });

    const sorted = scored.sort((a, b) => b.feasibilityScore - a.feasibilityScore).slice(0, 3);

    setTimeout(() => {
      setResults(sorted);
      setLoading(false);
    }, 1000);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    calculateRecommendations();
  };

  if (results) {
    return (
      <div className="space-y-6">
        <motion.h2 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-2xl font-semibold text-white mb-6"
        >
          Your Career Recommendations
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
                  <h3 className="text-xl font-semibold text-white">{result.name}</h3>
                  <span className="px-3 py-1 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 border border-purple-500/30 rounded-full text-sm text-cyan-400">
                    Rank #{index + 1}
                  </span>
                </div>
              </div>
              <div className="ml-4 text-3xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
                {result.feasibilityScore}%
              </div>
            </div>

            <div className="mb-4">
              <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: `${result.feasibilityScore}%` }}
                  transition={{ duration: 1, delay: index * 0.1 + 0.3 }}
                  className="h-full bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div className="p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg backdrop-blur-sm">
                <p className="text-xs text-gray-400 mb-1">Duration</p>
                <p className="text-sm font-semibold text-white">{result.duration}</p>
              </div>
              <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg backdrop-blur-sm">
                <p className="text-xs text-gray-400 mb-1">Avg Cost</p>
                <p className="text-sm font-semibold text-white">₹{(result.avgCost / 100000).toFixed(1)}L</p>
              </div>
              <div className="p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg backdrop-blur-sm">
                <p className="text-xs text-gray-400 mb-1">ROI</p>
                <p className="text-sm font-semibold text-white">{result.roi}/10</p>
              </div>
              <div className="p-3 bg-orange-500/10 border border-orange-500/30 rounded-lg backdrop-blur-sm">
                <p className="text-xs text-gray-400 mb-1">Demand</p>
                <p className="text-sm font-semibold text-white">{result.demand}</p>
              </div>
            </div>

            <div className="p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-lg backdrop-blur-sm">
              <div className="flex items-start space-x-2">
                <TrendingUp className="w-5 h-5 text-cyan-400 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-300">
                  This career path has a feasibility score of {result.feasibilityScore}% based on your budget, 
                  ROI potential, and market demand.
                </p>
              </div>
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
        After 12th Career Guidance
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
            Your Stream
          </label>
          <select
            value={formData.stream}
            onChange={(e) => setFormData({ ...formData, stream: e.target.value })}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300"
            required
          >
            <option value="" className="bg-slate-800">Select your stream</option>
            {streams.map((stream) => (
              <option key={stream.value} value={stream.value} className="bg-slate-800">
                {stream.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Budget Range
          </label>
          <select
            value={formData.budget}
            onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300"
            required
          >
            <option value="" className="bg-slate-800">Select budget range</option>
            {budgets.map((budget) => (
              <option key={budget.value} value={budget.value} className="bg-slate-800">
                {budget.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Career Preference
          </label>
          <select
            value={formData.preference}
            onChange={(e) => setFormData({ ...formData, preference: e.target.value })}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300"
            required
          >
            <option value="" className="bg-slate-800">Select preference</option>
            {preferences.map((pref) => (
              <option key={pref.value} value={pref.value} className="bg-slate-800">
                {pref.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex justify-center pt-4">
          <Button type="submit" variant="primary" disabled={loading}>
            {loading ? 'Analyzing...' : 'Get Recommendations'}
          </Button>
        </div>
      </motion.form>
    </div>
  );
};

export default After12thGuidance;
