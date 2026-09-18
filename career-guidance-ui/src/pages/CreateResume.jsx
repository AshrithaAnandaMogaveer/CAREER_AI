import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { FileText, ArrowLeft } from 'lucide-react';
import Button from '../components/Button';

const CreateResume = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-primary pt-32 pb-20 px-6">
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{ duration: 20, repeat: Infinity }}
          className="absolute top-1/4 right-1/4 w-96 h-96 bg-cyan-600/20 rounded-full blur-3xl"
        />
      </div>

      <div className="max-w-4xl mx-auto relative z-10">
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

        {/* Content */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="w-32 h-32 mx-auto mb-8 rounded-full bg-gradient-to-br from-cyan-500/20 to-blue-500/20 flex items-center justify-center glow-cyan"
          >
            <FileText className="w-16 h-16 text-cyan-400" />
          </motion.div>

          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              Resume Builder
            </span>
          </h1>

          <p className="text-gray-400 text-xl mb-8 max-w-2xl mx-auto">
            AI-powered resume builder to help you create professional resumes.
          </p>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="glass rounded-2xl p-8 max-w-2xl mx-auto mb-8"
          >
            <h2 className="text-2xl font-bold text-white mb-4">What to Expect</h2>
            <ul className="text-left text-gray-400 space-y-3">
              <li className="flex items-start space-x-3">
                <span className="text-cyan-400 mt-1">✓</span>
                <span>AI-powered resume templates</span>
              </li>
              <li className="flex items-start space-x-3">
                <span className="text-cyan-400 mt-1">✓</span>
                <span>Automatic skill highlighting</span>
              </li>
              <li className="flex items-start space-x-3">
                <span className="text-cyan-400 mt-1">✓</span>
                <span>ATS-friendly formatting</span>
              </li>
              <li className="flex items-start space-x-3">
                <span className="text-cyan-400 mt-1">✓</span>
                <span>Export to PDF/DOCX</span>
              </li>
              <li className="flex items-start space-x-3">
                <span className="text-cyan-400 mt-1">✓</span>
                <span>Real-time preview</span>
              </li>
            </ul>
          </motion.div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button variant="primary" onClick={() => navigate('/build-resume')}>
              Start Building Resume
            </Button>
            <Button variant="secondary" onClick={() => navigate('/analyze')}>
              Back to Analyze
            </Button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default CreateResume;
