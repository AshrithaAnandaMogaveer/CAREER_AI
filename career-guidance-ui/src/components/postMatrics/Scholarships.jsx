import { useState } from 'react';
import { motion } from 'framer-motion';
import { Award, IndianRupee, Users, GraduationCap } from 'lucide-react';
import Button from '../Button';

const Scholarships = () => {
  const [formData, setFormData] = useState({
    incomeRange: '',
    category: '',
    educationLevel: '',
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const incomeRanges = [
    { value: 'below1', label: 'Below ₹1 Lakh/year' },
    { value: '1to3', label: '₹1-3 Lakhs/year' },
    { value: '3to6', label: '₹3-6 Lakhs/year' },
    { value: 'above6', label: 'Above ₹6 Lakhs/year' },
  ];

  const categories = [
    { value: 'general', label: 'General' },
    { value: 'obc', label: 'OBC' },
    { value: 'sc', label: 'SC' },
    { value: 'st', label: 'ST' },
    { value: 'ews', label: 'EWS' },
    { value: 'pwd', label: 'PWD (Persons with Disabilities)' },
  ];

  const educationLevels = [
    { value: '10th', label: 'After 10th' },
    { value: '12th', label: 'After 12th' },
    { value: 'undergraduate', label: 'Undergraduate' },
    { value: 'postgraduate', label: 'Postgraduate' },
  ];

  const scholarshipDatabase = [
    {
      name: 'National Means-cum-Merit Scholarship',
      amount: 12000,
      eligibility: { income: ['below1', '1to3'], category: ['all'], education: ['10th', '12th'] },
      provider: 'Central Government',
      benefits: '₹12,000/year',
    },
    {
      name: 'Post Matric Scholarship (SC/ST)',
      amount: 50000,
      eligibility: { income: ['below1', '1to3', '3to6'], category: ['sc', 'st'], education: ['12th', 'undergraduate', 'postgraduate'] },
      provider: 'State Government',
      benefits: 'Up to ₹50,000/year',
    },
    {
      name: 'Pre Matric Scholarship (SC/ST)',
      amount: 10000,
      eligibility: { income: ['below1', '1to3'], category: ['sc', 'st'], education: ['10th'] },
      provider: 'State Government',
      benefits: '₹10,000/year',
    },
    {
      name: 'OBC Post Matric Scholarship',
      amount: 40000,
      eligibility: { income: ['below1', '1to3', '3to6'], category: ['obc'], education: ['12th', 'undergraduate', 'postgraduate'] },
      provider: 'State Government',
      benefits: 'Up to ₹40,000/year',
    },
    {
      name: 'EWS Scholarship',
      amount: 30000,
      eligibility: { income: ['below1', '1to3', '3to6'], category: ['ews'], education: ['12th', 'undergraduate', 'postgraduate'] },
      provider: 'Central Government',
      benefits: 'Up to ₹30,000/year',
    },
    {
      name: 'PWD Scholarship',
      amount: 50000,
      eligibility: { income: ['below1', '1to3', '3to6', 'above6'], category: ['pwd'], education: ['10th', '12th', 'undergraduate', 'postgraduate'] },
      provider: 'Central Government',
      benefits: 'Up to ₹50,000/year',
    },
    {
      name: 'Merit-cum-Means Scholarship',
      amount: 20000,
      eligibility: { income: ['below1', '1to3', '3to6'], category: ['all'], education: ['undergraduate', 'postgraduate'] },
      provider: 'UGC',
      benefits: '₹20,000/year',
    },
    {
      name: 'Prime Minister Scholarship Scheme',
      amount: 25000,
      eligibility: { income: ['below1', '1to3', '3to6'], category: ['all'], education: ['12th', 'undergraduate'] },
      provider: 'Central Government',
      benefits: '₹25,000/year',
    },
    {
      name: 'Inspire Scholarship',
      amount: 80000,
      eligibility: { income: ['below1', '1to3', '3to6', 'above6'], category: ['all'], education: ['undergraduate', 'postgraduate'] },
      provider: 'DST',
      benefits: '₹80,000/year',
    },
    {
      name: 'Minority Scholarship',
      amount: 30000,
      eligibility: { income: ['below1', '1to3', '3to6'], category: ['all'], education: ['12th', 'undergraduate', 'postgraduate'] },
      provider: 'Ministry of Minority Affairs',
      benefits: 'Up to ₹30,000/year',
    },
  ];

  const calculateRecommendations = () => {
    setLoading(true);

    const eligible = scholarshipDatabase.filter(scholarship => {
      const incomeMatch = scholarship.eligibility.income.includes(formData.incomeRange);
      const categoryMatch = scholarship.eligibility.category.includes('all') || 
                           scholarship.eligibility.category.includes(formData.category);
      const educationMatch = scholarship.eligibility.education.includes(formData.educationLevel);

      return incomeMatch && categoryMatch && educationMatch;
    });

    const sorted = eligible.sort((a, b) => b.amount - a.amount);

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
          Available Scholarships
        </motion.h2>
        
        {results.length === 0 ? (
          <div className="glass rounded-lg p-6 text-center glow-violet">
            <p className="text-yellow-400">No scholarships match your criteria. Try adjusting your filters or check state-specific scholarships.</p>
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
                    <Award className="w-6 h-6 text-cyan-400" />
                    <h3 className="text-xl font-semibold text-white">{result.name}</h3>
                  </div>
                  <p className="text-gray-400 text-sm">{result.provider}</p>
                </div>
                <div className="ml-4 flex flex-col items-end">
                  <div className="flex items-center space-x-1 text-2xl font-bold text-green-400">
                    <IndianRupee className="w-6 h-6" />
                    <span>{(result.amount / 1000).toFixed(0)}K</span>
                  </div>
                  <span className="text-xs text-gray-400">per year</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg backdrop-blur-sm">
                  <div className="flex items-center space-x-2 mb-1">
                    <IndianRupee className="w-4 h-4 text-green-400" />
                    <p className="text-xs text-gray-400">Benefits</p>
                  </div>
                  <p className="text-sm font-semibold text-white">{result.benefits}</p>
                </div>
                <div className="p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg backdrop-blur-sm">
                  <div className="flex items-center space-x-2 mb-1">
                    <Users className="w-4 h-4 text-blue-400" />
                    <p className="text-xs text-gray-400">Provider</p>
                  </div>
                  <p className="text-sm font-semibold text-white">{result.provider}</p>
                </div>
              </div>

              <div className="p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg backdrop-blur-sm">
                <div className="flex items-start space-x-2">
                  <GraduationCap className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-xs text-gray-400 mb-1">Eligibility</p>
                    <p className="text-sm text-gray-300">
                      Income: {result.eligibility.income.join(', ')} | 
                      Category: {result.eligibility.category.includes('all') ? 'All' : result.eligibility.category.join(', ').toUpperCase()} | 
                      Education: {result.eligibility.education.join(', ')}
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))
        )}

        <div className="glass rounded-lg p-4 glow-cyan">
          <p className="text-sm text-gray-300">
            <strong className="text-cyan-400">Note:</strong> These are indicative scholarships. Please visit the National Scholarship Portal (NSP) 
            or your state scholarship portal for complete details and application procedures.
          </p>
        </div>

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
        Find Scholarships
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
            Family Income Range
          </label>
          <select
            value={formData.incomeRange}
            onChange={(e) => setFormData({ ...formData, incomeRange: e.target.value })}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300"
            required
          >
            <option value="" className="bg-slate-800">Select income range</option>
            {incomeRanges.map((range) => (
              <option key={range.value} value={range.value} className="bg-slate-800">
                {range.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Category
          </label>
          <select
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-all duration-300"
            required
          >
            <option value="" className="bg-slate-800">Select category</option>
            {categories.map((cat) => (
              <option key={cat.value} value={cat.value} className="bg-slate-800">
                {cat.label}
              </option>
            ))}
          </select>
        </div>

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

        <div className="flex justify-center pt-4">
          <Button type="submit" variant="primary" disabled={loading}>
            {loading ? 'Finding Scholarships...' : 'Find Scholarships'}
          </Button>
        </div>
      </motion.form>
    </div>
  );
};

export default Scholarships;
