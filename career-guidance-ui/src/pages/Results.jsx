import React from 'react';
import { motion } from 'framer-motion';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  CheckCircle, XCircle, TrendingUp, Target, ArrowLeft, Download,
  Award, Briefcase, AlertTriangle, Lightbulb, BarChart3
} from 'lucide-react';
import Button from '../components/Button';

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const data = location.state;

  // Redirect if no data
  if (!data || !data.analysis) {
    navigate('/analyze');
    return null;
  }

  const { analysis, pdfReport } = data;

  const handleDownloadPDF = () => {
    if (!pdfReport) {
      alert('PDF report not available');
      return;
    }

    // Convert base64 to blob
    const byteCharacters = atob(pdfReport);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'application/pdf' });

    // Create download link
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `CareerAI_Analysis_Report_${new Date().toISOString().split('T')[0]}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getConfidenceColor = (level) => {
    if (level === 'High') return 'text-green-400';
    if (level === 'Medium') return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="min-h-screen bg-[#0f0f1a] pt-32 pb-20 px-6">
      <div className="max-w-7xl mx-auto relative z-10">
        {/* Back Button */}
        <motion.button
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          onClick={() => navigate('/analyze')}
          className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors mb-8"
        >
          <ArrowLeft size={20} />
          <span>Back to Analyze</span>
        </motion.button>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-4 text-white">
            Your Career Analysis
          </h1>
          <p className="text-gray-400 text-lg">
            Comprehensive insights based on your profile
          </p>
        </motion.div>

        {/* Score Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Readiness Score */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="bg-[#161625] rounded-xl p-6 border border-gray-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-lg bg-[#00cccc]/10 border border-[#00cccc]/30 flex items-center justify-center">
                <Target className="w-6 h-6 text-[#00cccc]" />
              </div>
              <div className={`text-4xl font-bold ${getScoreColor(analysis.readiness_score)}`}>
                {analysis.readiness_score}%
              </div>
            </div>
            <h3 className="text-lg font-semibold text-white mb-1">Career Readiness</h3>
            <p className="text-gray-400 text-sm">Overall preparedness score</p>
          </motion.div>

          {/* Resume Strength */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="bg-[#161625] rounded-xl p-6 border border-gray-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-lg bg-[#6b46c1]/10 border border-[#6b46c1]/30 flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-[#6b46c1]" />
              </div>
              <div className={`text-4xl font-bold ${getScoreColor(analysis.resume_strength)}`}>
                {analysis.resume_strength}%
              </div>
            </div>
            <h3 className="text-lg font-semibold text-white mb-1">Resume Strength</h3>
            <p className="text-gray-400 text-sm">Quality and completeness</p>
          </motion.div>

          {/* Confidence Level */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="bg-[#161625] rounded-xl p-6 border border-gray-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-lg bg-green-500/10 border border-green-500/30 flex items-center justify-center">
                <Award className="w-6 h-6 text-green-400" />
              </div>
              <div className={`text-2xl font-bold ${getConfidenceColor(analysis.confidence_level)}`}>
                {analysis.confidence_level}
              </div>
            </div>
            <h3 className="text-lg font-semibold text-white mb-1">Confidence Level</h3>
            <p className="text-gray-400 text-sm">Analysis reliability</p>
          </motion.div>
        </div>

        {/* Skills Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          {/* Your Skills */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="bg-[#161625] rounded-xl p-6 border border-gray-700"
          >
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 rounded-lg bg-green-500/10 border border-green-500/30 flex items-center justify-center">
                <CheckCircle className="w-5 h-5 text-green-400" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Your Skills</h2>
                <p className="text-gray-400 text-sm">{analysis.total_skills} skills identified</p>
              </div>
            </div>

            <div className="max-h-96 overflow-y-auto space-y-2">
              {analysis.extracted_skills && analysis.extracted_skills.length > 0 ? (
                analysis.extracted_skills.map((skill, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 + index * 0.05 }}
                    className="flex items-center space-x-2 p-3 bg-[#0f0f1a] rounded-lg border border-gray-700"
                  >
                    <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0" />
                    <span className="text-white text-sm">{skill}</span>
                  </motion.div>
                ))
              ) : (
                <p className="text-gray-400">No skills extracted</p>
              )}
            </div>
          </motion.div>

          {/* Missing Skills */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="bg-[#161625] rounded-xl p-6 border border-gray-700"
          >
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 rounded-lg bg-red-500/10 border border-red-500/30 flex items-center justify-center">
                <XCircle className="w-5 h-5 text-red-400" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Skill Gaps</h2>
                <p className="text-gray-400 text-sm">Skills to develop</p>
              </div>
            </div>

            <div className="max-h-96 overflow-y-auto space-y-4">
              {/* Critical Skills */}
              {analysis.missing_skills?.critical && analysis.missing_skills.critical.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-red-400 mb-2">Critical Skills</h3>
                  <div className="space-y-2">
                    {analysis.missing_skills.critical.map((skill, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.6 + index * 0.05 }}
                        className="flex items-center space-x-2 p-3 bg-[#0f0f1a] rounded-lg border border-red-500/30"
                      >
                        <XCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
                        <span className="text-white text-sm">{skill}</span>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}

              {/* Recommended Skills */}
              {analysis.missing_skills?.recommended && analysis.missing_skills.recommended.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-yellow-400 mb-2">Recommended Skills</h3>
                  <div className="space-y-2">
                    {analysis.missing_skills.recommended.slice(0, 5).map((skill, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.7 + index * 0.05 }}
                        className="flex items-center space-x-2 p-3 bg-[#0f0f1a] rounded-lg border border-yellow-500/30"
                      >
                        <AlertTriangle className="w-4 h-4 text-yellow-400 flex-shrink-0" />
                        <span className="text-white text-sm">{skill}</span>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        </div>

        {/* Suggestions */}
        {analysis.suggestions && analysis.suggestions.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="bg-[#161625] rounded-xl p-6 border border-gray-700 mb-8"
          >
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 rounded-lg bg-[#00cccc]/10 border border-[#00cccc]/30 flex items-center justify-center">
                <Lightbulb className="w-5 h-5 text-[#00cccc]" />
              </div>
              <h2 className="text-xl font-bold text-white">Personalized Recommendations</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {analysis.suggestions.map((suggestion, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 + index * 0.1 }}
                  className="p-4 bg-[#0f0f1a] rounded-lg border border-gray-700"
                >
                  <p className="text-white text-sm">{suggestion}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Suggested Domains */}
        {analysis.suggested_domains && analysis.suggested_domains.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.7 }}
            className="bg-[#161625] rounded-xl p-6 border border-gray-700 mb-8"
          >
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 rounded-lg bg-[#6b46c1]/10 border border-[#6b46c1]/30 flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-[#6b46c1]" />
              </div>
              <h2 className="text-xl font-bold text-white">Recommended Career Paths</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {analysis.suggested_domains.map((domain, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.8 + index * 0.1 }}
                  className="p-6 bg-[#0f0f1a] rounded-lg border border-gray-700 hover:border-[#6b46c1] transition-all duration-200"
                >
                  <div className="text-center">
                    <div className="text-3xl font-bold text-[#6b46c1] mb-2">
                      {domain.match_percentage}%
                    </div>
                    <h3 className="text-white font-semibold mb-2">{domain.domain}</h3>
                    <p className="text-gray-400 text-sm">
                      {domain.matched_skills}/{domain.total_skills} skills matched
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.8 }}
        >
          {/* Smart Navigation Banner */}
          <div className="bg-[#161625] border border-[#00cccc]/20 rounded-xl p-5 mb-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <p className="text-[#00cccc] text-xs font-semibold tracking-widest uppercase mb-1">Next Step</p>
              <p className="text-white font-semibold">
                You are {analysis.readiness_score}% ready
                {analysis.suggested_domains?.[0]?.domain ? ` for ${analysis.suggested_domains[0].domain}` : ''}
              </p>
              <p className="text-gray-400 text-xs mt-0.5">Explore personalized career insights based on your analysis</p>
            </div>
            <button
              onClick={() => navigate('/explore')}
              className="flex-shrink-0 px-5 py-2.5 bg-[#00cccc] text-[#0f0f1a] font-semibold rounded-lg text-sm hover:bg-[#00aaaa] transition-colors"
            >
              Explore Career Insights →
            </button>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              variant="primary"
              onClick={handleDownloadPDF}
              className="flex items-center justify-center space-x-2"
            >
              <Download size={20} />
              <span>Download PDF Report</span>
            </Button>
            <Button variant="secondary" onClick={() => navigate('/analyze')}>
              Analyze Again
            </Button>
            <Button variant="secondary" onClick={() => navigate('/')}>
              Back to Home
            </Button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Results;
