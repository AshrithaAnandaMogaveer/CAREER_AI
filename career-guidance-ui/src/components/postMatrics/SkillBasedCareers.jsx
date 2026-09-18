import { useState } from 'react';
import { motion } from 'framer-motion';
import { Briefcase, Wifi, DollarSign, TrendingUp } from 'lucide-react';
import Button from '../Button';

const SkillBasedCareers = () => {
  const [formData, setFormData] = useState({ educationLevel: '', internetAccess: '', investmentCapability: '' });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const educationLevels = [
    { value: '10th', label: 'After 10th' }, { value: '12th', label: 'After 12th' },
    { value: 'graduate', label: 'Graduate' }, { value: 'any', label: 'Any' }
  ];

  const internetOptions = [
    { value: 'none', label: 'No Internet', multiplier: 0.5 },
    { value: 'limited', label: 'Limited Internet', multiplier: 0.8 },
    { value: 'good', label: 'Good Internet', multiplier: 1.2 }
  ];

  const investmentOptions = [
    { value: 'zero', label: '₹0 (Free)', multiplier: 1.0 }, { value: 'low', label: '< ₹10,000', multiplier: 1.2 },
    { value: 'medium', label: '₹10,000 - ₹50,000', multiplier: 1.4 }, { value: 'high', label: '> ₹50,000', multiplier: 1.6 }
  ];

  const careerDatabase = [
    { name: 'Web Development', minEducation: 'any', internetRequired: 'good', minInvestment: 'zero', avgIncome: 40000, accessibility: 85, learningTime: '6-12 months' },
    { name: 'Graphic Design', minEducation: 'any', internetRequired: 'limited', minInvestment: 'low', avgIncome: 30000, accessibility: 80, learningTime: '4-8 months' },
    { name: 'Digital Marketing', minEducation: '12th', internetRequired: 'good', minInvestment: 'zero', avgIncome: 35000, accessibility: 90, learningTime: '3-6 months' },
    { name: 'Content Writing', minEducation: '12th', internetRequired: 'good', minInvestment: 'zero', avgIncome: 25000, accessibility: 95, learningTime: '2-4 months' },
    { name: 'Video Editing', minEducation: 'any', internetRequired: 'limited', minInvestment: 'medium', avgIncome: 35000, accessibility: 75, learningTime: '4-8 months' },
    { name: 'Data Entry', minEducation: '10th', internetRequired: 'limited', minInvestment: 'zero', avgIncome: 15000, accessibility: 100, learningTime: '1-2 months' },
    { name: 'Mobile App Development', minEducation: '12th', internetRequired: 'good', minInvestment: 'low', avgIncome: 50000, accessibility: 70, learningTime: '8-12 months' },
    { name: 'Social Media Management', minEducation: '12th', internetRequired: 'good', minInvestment: 'zero', avgIncome: 30000, accessibility: 85, learningTime: '2-4 months' },
    { name: 'Photography', minEducation: 'any', internetRequired: 'limited', minInvestment: 'high', avgIncome: 40000, accessibility: 60, learningTime: '6-12 months' },
    { name: 'Accounting/Tally', minEducation: '12th', internetRequired: 'none', minInvestment: 'low', avgIncome: 20000, accessibility: 80, learningTime: '3-6 months' }
  ];

  const educationHierarchy = { 'any': 0, '10th': 1, '12th': 2, 'graduate': 3 };
  const internetHierarchy = { 'none': 0, 'limited': 1, 'good': 2 };
  const investmentHierarchy = { 'zero': 0, 'low': 1, 'medium': 2, 'high': 3 };

  const calculateRecommendations = () => {
    setLoading(true);
    const userEducation = educationHierarchy[formData.educationLevel];
    const userInternet = internetHierarchy[formData.internetAccess];
    const userInvestment = investmentHierarchy[formData.investmentCapability];
    const internetMultiplier = internetOptions.find(i => i.value === formData.internetAccess)?.multiplier || 1.0;
    const investmentMultiplier = investmentOptions.find(i => i.value === formData.investmentCapability)?.multiplier || 1.0;

    const eligible = careerDatabase.filter(career => {
      const careerEducation = educationHierarchy[career.minEducation];
      const careerInternet = internetHierarchy[career.internetRequired];
      const careerInvestment = investmentHierarchy[career.minInvestment];
      return userEducation >= careerEducation && userInternet >= careerInternet && userInvestment >= careerInvestment;
    });

    const scored = eligible.map(career => {
      let score = career.accessibility + (career.avgIncome / 1000) * 0.5;
      score *= internetMultiplier * investmentMultiplier;
      return { ...career, accessibilityScore: Math.min(100, Math.round(score)) };
    });

    const sorted = scored.sort((a, b) => b.accessibilityScore - a.accessibilityScore).slice(0, 5);
    setTimeout(() => { setResults(sorted); setLoading(false); }, 1000);
  };

  const handleSubmit = (e) => { e.preventDefault(); calculateRecommendations(); };

  if (results) {
    return (
      <div className="space-y-6">
        <motion.h2 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-2xl font-semibold text-white mb-6"
        >
          Recommended Skill-Based Careers
        </motion.h2>
        {results.length === 0 ? (
          <div className="glass rounded-lg p-6 text-center glow-violet">
            <p className="text-yellow-400">No careers match your current criteria. Try adjusting your filters.</p>
          </div>
        ) : (
          results.map((result, index) => (
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
                    <Briefcase className="w-6 h-6 text-cyan-400" />
                    <h3 className="text-xl font-semibold text-white">{result.name}</h3>
                    <span className="px-3 py-1 bg-gradient-to-r from-purple-500/20 to-cyan-500/20 border border-purple-500/30 rounded-full text-sm text-cyan-400">Rank #{index + 1}</span>
                  </div>
                </div>
                <div className="ml-4 text-3xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">{result.accessibilityScore}%</div>
              </div>
              <div className="mb-4">
                <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: `${result.accessibilityScore}%` }}
                    transition={{ duration: 1, delay: index * 0.1 + 0.3 }}
                    className="h-full bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg backdrop-blur-sm">
                  <div className="flex items-center space-x-2 mb-1"><DollarSign className="w-4 h-4 text-green-400" /><p className="text-xs text-gray-400">Avg Income</p></div>
                  <p className="text-sm font-semibold text-white">₹{result.avgIncome.toLocaleString()}/mo</p>
                </div>
                <div className="p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg backdrop-blur-sm">
                  <div className="flex items-center space-x-2 mb-1"><Wifi className="w-4 h-4 text-blue-400" /><p className="text-xs text-gray-400">Internet</p></div>
                  <p className="text-sm font-semibold text-white capitalize">{result.internetRequired}</p>
                </div>
                <div className="p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg backdrop-blur-sm">
                  <p className="text-xs text-gray-400 mb-1">Min Education</p>
                  <p className="text-sm font-semibold text-white capitalize">{result.minEducation}</p>
                </div>
                <div className="p-3 bg-orange-500/10 border border-orange-500/30 rounded-lg backdrop-blur-sm">
                  <div className="flex items-center space-x-2 mb-1"><TrendingUp className="w-4 h-4 text-orange-400" /><p className="text-xs text-gray-400">Learning Time</p></div>
                  <p className="text-sm font-semibold text-white">{result.learningTime}</p>
                </div>
              </div>
              <div className="p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-lg backdrop-blur-sm">
                <p className="text-sm text-gray-300">This career has an accessibility score of {result.accessibilityScore}% based on your education, internet access, and investment capability.</p>
              </div>
            </motion.div>
          ))
        )}
        <div className="text-center"><Button variant="secondary" onClick={() => setResults(null)}>Try Again</Button></div>
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
        Explore Skill-Based Careers
      </motion.h2>
      <motion.form 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        onSubmit={handleSubmit} 
        className="space-y-6"
      >
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Education Level</label>
          <select value={formData.educationLevel} onChange={(e) => setFormData({ ...formData, educationLevel: e.target.value })} className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300" required>
            <option value="" className="bg-slate-800">Select education level</option>
            {educationLevels.map((level) => (<option key={level.value} value={level.value} className="bg-slate-800">{level.label}</option>))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Internet Access</label>
          <select value={formData.internetAccess} onChange={(e) => setFormData({ ...formData, internetAccess: e.target.value })} className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300" required>
            <option value="" className="bg-slate-800">Select internet access</option>
            {internetOptions.map((option) => (<option key={option.value} value={option.value} className="bg-slate-800">{option.label}</option>))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Investment Capability</label>
          <select value={formData.investmentCapability} onChange={(e) => setFormData({ ...formData, investmentCapability: e.target.value })} className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300" required>
            <option value="" className="bg-slate-800">Select investment capability</option>
            {investmentOptions.map((option) => (<option key={option.value} value={option.value} className="bg-slate-800">{option.label}</option>))}
          </select>
        </div>
        <div className="flex justify-center pt-4"><Button type="submit" variant="primary" disabled={loading}>{loading ? 'Finding Careers...' : 'Find Careers'}</Button></div>
      </motion.form>
    </div>
  );
};

export default SkillBasedCareers;
