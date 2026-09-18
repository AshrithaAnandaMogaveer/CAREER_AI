import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import ResumeTemplateSelector from '../components/resume/ResumeTemplateSelector';
import ResumeForm from '../components/resume/ResumeForm';
import ResumePreview from '../components/resume/ResumePreview';
import DownloadButtons from '../components/resume/DownloadButtons';
import ATSScoreBadge from '../components/resume/ATSScoreBadge';
import ResumeToolbar from '../components/resume/ResumeToolbar';

const BuildResume = () => {
  const navigate = useNavigate();
  const [selectedTemplate, setSelectedTemplate] = useState('modern');
  const [previewTheme, setPreviewTheme] = useState('light');
  const [resumeData, setResumeData] = useState({
    personalInfo: {
      name: '',
      email: '',
      phone: '',
      linkedin: '',
      github: '',
      location: '',
    },
    summary: '',
    skills: [],
    experience: [],
    education: [],
    projects: [],
    certifications: [],
    achievements: [],
  });

  const handleDataChange = (section, data) => {
    setResumeData(prev => ({
      ...prev,
      [section]: data,
    }));
  };

  const togglePreviewTheme = () => {
    setPreviewTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <div className="min-h-screen bg-[#0f0f1a] pt-24 pb-20 px-4 md:px-6">
      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Button
            variant="secondary"
            onClick={() => navigate('/analyze')}
            className="flex items-center space-x-2"
          >
            <ArrowLeft size={18} />
            <span>Back</span>
          </Button>

          <h1 className="text-3xl md:text-4xl font-bold text-white">
            Resume Builder
          </h1>

          <DownloadButtons 
            resumeData={resumeData} 
            selectedTemplate={selectedTemplate}
            previewTheme="light"
          />
        </div>

        {/* ATS Score Badge */}
        <div className="mb-6">
          <ATSScoreBadge resumeData={resumeData} />
        </div>

        {/* Template Selector */}
        <div className="mb-6">
          <ResumeTemplateSelector
            selectedTemplate={selectedTemplate}
            onSelectTemplate={setSelectedTemplate}
          />
        </div>

        {/* Split Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left: Form */}
          <div
            className="bg-[#161625] rounded-xl p-6 border border-gray-700 overflow-y-auto"
            style={{ maxHeight: 'calc(100vh - 250px)' }}
          >
            <ResumeForm resumeData={resumeData} onDataChange={handleDataChange} />
          </div>

          {/* Right: Preview */}
          <div
            className="bg-[#161625] rounded-xl p-6 border border-gray-700 overflow-y-auto"
            style={{ maxHeight: 'calc(100vh - 250px)' }}
          >
            <ResumeToolbar 
              previewTheme={previewTheme}
              onThemeToggle={togglePreviewTheme}
            />
            <ResumePreview 
              resumeData={resumeData} 
              template={selectedTemplate}
              previewMode={true}
              previewTheme={previewTheme}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default BuildResume;
