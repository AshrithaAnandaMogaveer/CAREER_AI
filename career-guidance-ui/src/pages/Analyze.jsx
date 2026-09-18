import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { FileText, Edit, X, Loader, Download } from 'lucide-react';
import FileUpload from '../components/FileUpload';
import SelectField from '../components/SelectField';
import InputField from '../components/InputField';
import Button from '../components/Button';
import { analyzeResumeComprehensive } from '../services/analyzeService';

const Analyze = () => {
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Form data
  const [formData, setFormData] = useState({
    currentDomain: '',
    targetDomain: '',
    experienceYears: '',
    manualSkills: '',
    projectDescriptions: '',
    certifications: '',
    strengthLevel: 'Intermediate',
  });

  const domains = [
    'Software Development',
    'Data Science',
    'Machine Learning',
    'Web Development',
    'Mobile Development',
    'DevOps',
    'Cybersecurity',
    'Cloud Computing',
    'UI/UX Design',
    'Product Management',
  ];

  const strengthLevels = ['Beginner', 'Intermediate', 'Advanced'];

  const openModal = () => {
    setIsModalOpen(true);
    setError('');
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedFile(null);
    setFormData({
      currentDomain: '',
      targetDomain: '',
      experienceYears: '',
      manualSkills: '',
      projectDescriptions: '',
      certifications: '',
      strengthLevel: 'Intermediate',
    });
    setError('');
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    // Validation
    if (!selectedFile && !formData.manualSkills.trim()) {
      setError('Please upload a resume or enter your skills manually');
      return;
    }

    if (!formData.targetDomain) {
      setError('Please select your target domain');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await analyzeResumeComprehensive({
        file: selectedFile,
        ...formData,
      });

      if (response.success) {
        // Save targetDomain so Routine Build can use it
        localStorage.setItem('analyzeTargetDomain', formData.targetDomain);

        // Navigate to results page with comprehensive data
        navigate('/results', {
          state: {
            analysis: response.analysis,
            pdfReport: response.pdf_report,
          },
        });
      } else {
        setError(response.message || 'Analysis failed. Please try again.');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0f0f1a] pt-32 pb-20 px-6">
      <div className="max-w-6xl mx-auto relative z-10">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-4 text-white">
            Analyze & Build
            <br />
            <span className="text-[#00cccc]">Your Career Path</span>
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Upload your resume or enter your skills to get personalized career insights
          </p>
        </motion.div>

        {/* Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Card 1: Analyze Resume/Skills */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            whileHover={{ y: -10 }}
            onClick={openModal}
            className="bg-[#161625] rounded-xl p-8 cursor-pointer border border-gray-700 hover:border-[#00cccc] transition-all duration-300"
          >
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="w-20 h-20 rounded-full bg-[#00cccc]/10 border border-[#00cccc]/30 flex items-center justify-center">
                <FileText className="w-10 h-10 text-[#00cccc]" />
              </div>
              <h2 className="text-2xl font-bold text-white">
                Analyze Your Profile
              </h2>
              <p className="text-gray-400 leading-relaxed">
                Upload your resume or manually enter your skills to get comprehensive career analysis
              </p>
            </div>
          </motion.div>

          {/* Card 2: Create Resume */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            whileHover={{ y: -10 }}
            onClick={() => navigate('/create-resume')}
            className="bg-[#161625] rounded-xl p-8 cursor-pointer border border-gray-700 hover:border-[#6b46c1] transition-all duration-300"
          >
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="w-20 h-20 rounded-full bg-[#6b46c1]/10 border border-[#6b46c1]/30 flex items-center justify-center">
                <Edit className="w-10 h-10 text-[#6b46c1]" />
              </div>
              <h2 className="text-2xl font-bold text-white">
                Create Resume
              </h2>
              <p className="text-gray-400 leading-relaxed">
                Build a professional resume with our AI-powered resume builder
              </p>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Enhanced Modal */}
      <AnimatePresence>
        {isModalOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={closeModal}
              className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
            />

            {/* Modal Content */}
            <div className="fixed inset-0 flex items-center justify-center z-50 p-4">
              <motion.div
                initial={{ opacity: 0, scale: 0.9, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.9, y: 20 }}
                transition={{ type: 'spring', duration: 0.5 }}
                className="bg-[#161625] rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto relative border border-gray-700"
                onClick={(e) => e.stopPropagation()}
              >
                {/* Close Button */}
                <button
                  onClick={closeModal}
                  className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors z-10"
                >
                  <X size={24} />
                </button>

                <div className="p-8">
                  {/* Modal Header */}
                  <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold text-white mb-2">
                      Career Analysis
                    </h2>
                    <p className="text-gray-400">
                      Provide your information for comprehensive analysis
                    </p>
                  </div>

                  {/* Form */}
                  <div className="space-y-6">
                    {/* Resume Upload */}
                    <div className="bg-[#0f0f1a] rounded-lg p-6 border border-gray-700">
                      <label className="block text-sm font-medium text-white mb-3">
                        Upload Resume (Optional)
                      </label>
                      <FileUpload
                        onFileSelect={setSelectedFile}
                        acceptedTypes=".pdf,.doc,.docx"
                      />
                      {selectedFile && (
                        <p className="text-[#00cccc] text-sm mt-2">
                          ✓ {selectedFile.name}
                        </p>
                      )}
                    </div>

                    {/* Domain Selection */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <SelectField
                        label="Current Domain"
                        name="currentDomain"
                        value={formData.currentDomain}
                        onChange={handleInputChange}
                        options={domains}
                      />
                      <SelectField
                        label="Target Domain"
                        name="targetDomain"
                        value={formData.targetDomain}
                        onChange={handleInputChange}
                        options={domains}
                        required
                      />
                    </div>

                    {/* Experience and Strength */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <InputField
                        label="Years of Experience"
                        name="experienceYears"
                        type="number"
                        value={formData.experienceYears}
                        onChange={handleInputChange}
                        placeholder="0"
                        min="0"
                      />
                      <SelectField
                        label="Strength Level"
                        name="strengthLevel"
                        value={formData.strengthLevel}
                        onChange={handleInputChange}
                        options={strengthLevels}
                      />
                    </div>

                    {/* Manual Skills */}
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Known Skills (comma-separated)
                      </label>
                      <textarea
                        name="manualSkills"
                        value={formData.manualSkills}
                        onChange={handleInputChange}
                        placeholder="e.g., Python, React, Machine Learning, Docker, AWS"
                        rows="3"
                        className="w-full px-4 py-3 bg-[#0f0f1a] border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:border-[#00cccc] transition-all duration-200 resize-none"
                      />
                    </div>

                    {/* Project Descriptions */}
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Project Descriptions (one per line)
                      </label>
                      <textarea
                        name="projectDescriptions"
                        value={formData.projectDescriptions}
                        onChange={handleInputChange}
                        placeholder="Describe your key projects..."
                        rows="4"
                        className="w-full px-4 py-3 bg-[#0f0f1a] border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:border-[#00cccc] transition-all duration-200 resize-none"
                      />
                    </div>

                    {/* Certifications */}
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Certifications (comma-separated)
                      </label>
                      <input
                        type="text"
                        name="certifications"
                        value={formData.certifications}
                        onChange={handleInputChange}
                        placeholder="e.g., AWS Certified, Google Cloud Professional"
                        className="w-full px-4 py-3 bg-[#0f0f1a] border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:border-[#00cccc] transition-all duration-200"
                      />
                    </div>

                    {/* Error Message */}
                    {error && (
                      <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm"
                      >
                        {error}
                      </motion.div>
                    )}

                    {/* Submit Button */}
                    <Button
                      onClick={handleSubmit}
                      variant="primary"
                      className="w-full"
                      disabled={isLoading}
                    >
                      {isLoading ? (
                        <span className="flex items-center justify-center">
                          <Loader className="animate-spin mr-2" size={20} />
                          Analyzing...
                        </span>
                      ) : (
                        'Analyze Now'
                      )}
                    </Button>
                  </div>
                </div>
              </motion.div>
            </div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Analyze;
