import { useState } from 'react';
import { ChevronDown, ChevronUp, Plus, Trash2 } from 'lucide-react';
import Button from '../Button';

// Section component defined outside to prevent re-creation on every render
const Section = ({ title, sectionKey, children, expandedSections, toggleSection }) => (
  <div className="mb-4">
    <button
      onClick={() => toggleSection(sectionKey)}
      className="w-full flex items-center justify-between p-3 bg-[#0f0f1a] rounded-lg border border-gray-700 hover:border-[#00cccc] transition-colors duration-200"
    >
      <h3 className="text-lg font-semibold text-white">{title}</h3>
      {expandedSections[sectionKey] ? (
        <ChevronUp className="text-gray-400" size={20} />
      ) : (
        <ChevronDown className="text-gray-400" size={20} />
      )}
    </button>

    {expandedSections[sectionKey] && (
      <div className="mt-3 space-y-3">
        {children}
      </div>
    )}
  </div>
);

const ResumeForm = ({ resumeData, onDataChange }) => {
  const [expandedSections, setExpandedSections] = useState({
    personalInfo: true,
    summary: true,
    skills: false,
    experience: false,
    education: false,
    projects: false,
    certifications: false,
    achievements: false,
  });

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const handlePersonalInfoChange = (field, value) => {
    onDataChange('personalInfo', {
      ...resumeData.personalInfo,
      [field]: value,
    });
  };

  const handleSummaryChange = (value) => {
    onDataChange('summary', value);
  };

  const handleSkillsChange = (skills) => {
    onDataChange('skills', skills);
  };

  const addSkill = () => {
    onDataChange('skills', [...resumeData.skills, { id: Date.now(), text: '' }]);
  };

  const updateSkill = (index, value) => {
    const newSkills = [...resumeData.skills];
    newSkills[index] = { ...newSkills[index], text: value };
    onDataChange('skills', newSkills);
  };

  const removeSkill = (index) => {
    onDataChange('skills', resumeData.skills.filter((_, i) => i !== index));
  };

  const addExperience = () => {
    onDataChange('experience', [
      ...resumeData.experience,
      { id: Date.now(), company: '', role: '', duration: '', description: '' },
    ]);
  };

  const updateExperience = (index, field, value) => {
    const newExperience = [...resumeData.experience];
    newExperience[index] = { ...newExperience[index], [field]: value };
    onDataChange('experience', newExperience);
  };

  const removeExperience = (index) => {
    onDataChange('experience', resumeData.experience.filter((_, i) => i !== index));
  };

  const addEducation = () => {
    onDataChange('education', [
      ...resumeData.education,
      { id: Date.now(), degree: '', institution: '', year: '', grade: '' },
    ]);
  };

  const updateEducation = (index, field, value) => {
    const newEducation = [...resumeData.education];
    newEducation[index] = { ...newEducation[index], [field]: value };
    onDataChange('education', newEducation);
  };

  const removeEducation = (index) => {
    onDataChange('education', resumeData.education.filter((_, i) => i !== index));
  };

  const addProject = () => {
    onDataChange('projects', [
      ...resumeData.projects,
      { id: Date.now(), title: '', techStack: '', description: '' },
    ]);
  };

  const updateProject = (index, field, value) => {
    const newProjects = [...resumeData.projects];
    newProjects[index] = { ...newProjects[index], [field]: value };
    onDataChange('projects', newProjects);
  };

  const removeProject = (index) => {
    onDataChange('projects', resumeData.projects.filter((_, i) => i !== index));
  };

  const addCertification = () => {
    onDataChange('certifications', [...resumeData.certifications, { id: Date.now(), text: '' }]);
  };

  const updateCertification = (index, value) => {
    const newCertifications = [...resumeData.certifications];
    newCertifications[index] = { ...newCertifications[index], text: value };
    onDataChange('certifications', newCertifications);
  };

  const removeCertification = (index) => {
    onDataChange('certifications', resumeData.certifications.filter((_, i) => i !== index));
  };

  const addAchievement = () => {
    onDataChange('achievements', [...resumeData.achievements, { id: Date.now(), text: '' }]);
  };

  const updateAchievement = (index, value) => {
    const newAchievements = [...resumeData.achievements];
    newAchievements[index] = { ...newAchievements[index], text: value };
    onDataChange('achievements', newAchievements);
  };

  const removeAchievement = (index) => {
    onDataChange('achievements', resumeData.achievements.filter((_, i) => i !== index));
  };

  const inputClass = "w-full px-4 py-2 bg-[#0f0f1a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#00cccc] focus:ring-1 focus:ring-[#00cccc] transition-colors duration-200 text-sm";
  const textareaClass = "w-full px-4 py-2 bg-[#0f0f1a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#00cccc] focus:ring-1 focus:ring-[#00cccc] transition-colors duration-200 text-sm resize-none";

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-white mb-6">Resume Details</h2>

      {/* Personal Information */}
      <Section title="Personal Information" sectionKey="personalInfo" expandedSections={expandedSections} toggleSection={toggleSection}>
        <input
          type="text"
          placeholder="Full Name"
          value={resumeData.personalInfo.name}
          onChange={(e) => handlePersonalInfoChange('name', e.target.value)}
          className={inputClass}
        />
        <input
          type="email"
          placeholder="Email"
          value={resumeData.personalInfo.email}
          onChange={(e) => handlePersonalInfoChange('email', e.target.value)}
          className={inputClass}
        />
        <input
          type="tel"
          placeholder="Phone"
          value={resumeData.personalInfo.phone}
          onChange={(e) => handlePersonalInfoChange('phone', e.target.value)}
          className={inputClass}
        />
        <input
          type="text"
          placeholder="LinkedIn URL"
          value={resumeData.personalInfo.linkedin}
          onChange={(e) => handlePersonalInfoChange('linkedin', e.target.value)}
          className={inputClass}
        />
        <input
          type="text"
          placeholder="GitHub URL"
          value={resumeData.personalInfo.github}
          onChange={(e) => handlePersonalInfoChange('github', e.target.value)}
          className={inputClass}
        />
        <input
          type="text"
          placeholder="Location"
          value={resumeData.personalInfo.location}
          onChange={(e) => handlePersonalInfoChange('location', e.target.value)}
          className={inputClass}
        />
      </Section>

      {/* Professional Summary */}
      <Section title="Professional Summary" sectionKey="summary" expandedSections={expandedSections} toggleSection={toggleSection}>
        <textarea
          placeholder="Write a brief professional summary..."
          value={resumeData.summary}
          onChange={(e) => handleSummaryChange(e.target.value)}
          rows="4"
          className={textareaClass}
        />
      </Section>

      {/* Skills */}
      <Section title="Skills" sectionKey="skills" expandedSections={expandedSections} toggleSection={toggleSection}>
        {resumeData.skills.map((skill, index) => (
          <div key={skill.id || `skill-${index}`} className="flex gap-2">
            <input
              type="text"
              placeholder="Skill name"
              value={typeof skill === 'string' ? skill : skill.text}
              onChange={(e) => updateSkill(index, e.target.value)}
              className={inputClass}
            />
            <button
              onClick={() => removeSkill(index)}
              className="p-2 bg-[#0f0f1a] border border-gray-700 rounded-lg hover:bg-red-500/20 hover:border-red-500 transition-colors"
            >
              <Trash2 size={18} className="text-red-400" />
            </button>
          </div>
        ))}
        <button
          onClick={addSkill}
          className="w-full p-2 bg-[#0f0f1a] border border-gray-700 rounded-lg hover:border-[#00cccc] transition-colors flex items-center justify-center space-x-2 text-[#00cccc]"
        >
          <Plus size={18} />
          <span>Add Skill</span>
        </button>
      </Section>

      {/* Experience */}
      <Section title="Experience" sectionKey="experience" expandedSections={expandedSections} toggleSection={toggleSection}>
        {resumeData.experience.map((exp, index) => (
          <div key={exp.id || `exp-${index}`} className="bg-[#0f0f1a] border border-gray-700 rounded-lg p-4 space-y-3">
            <div className="flex justify-between items-start">
              <h4 className="text-white font-medium">Experience {index + 1}</h4>
              <button
                onClick={() => removeExperience(index)}
                className="p-1 hover:bg-red-500/20 rounded transition-colors"
              >
                <Trash2 size={16} className="text-red-400" />
              </button>
            </div>
            <input
              type="text"
              placeholder="Company Name"
              value={exp.company}
              onChange={(e) => updateExperience(index, 'company', e.target.value)}
              className={inputClass}
            />
            <input
              type="text"
              placeholder="Role/Position"
              value={exp.role}
              onChange={(e) => updateExperience(index, 'role', e.target.value)}
              className={inputClass}
            />
            <input
              type="text"
              placeholder="Duration (e.g., Jan 2020 - Dec 2022)"
              value={exp.duration}
              onChange={(e) => updateExperience(index, 'duration', e.target.value)}
              className={inputClass}
            />
            <textarea
              placeholder="Description"
              value={exp.description}
              onChange={(e) => updateExperience(index, 'description', e.target.value)}
              rows="3"
              className={textareaClass}
            />
          </div>
        ))}
        <button
          onClick={addExperience}
          className="w-full p-2 bg-[#0f0f1a] border border-gray-700 rounded-lg hover:border-[#00cccc] transition-colors flex items-center justify-center space-x-2 text-[#00cccc]"
        >
          <Plus size={18} />
          <span>Add Experience</span>
        </button>
      </Section>

      {/* Education */}
      <Section title="Education" sectionKey="education" expandedSections={expandedSections} toggleSection={toggleSection}>
        {resumeData.education.map((edu, index) => (
          <div key={edu.id || `edu-${index}`} className="bg-[#0f0f1a] border border-gray-700 rounded-lg p-4 space-y-3">
            <div className="flex justify-between items-start">
              <h4 className="text-white font-medium">Education {index + 1}</h4>
              <button
                onClick={() => removeEducation(index)}
                className="p-1 hover:bg-red-500/20 rounded transition-colors"
              >
                <Trash2 size={16} className="text-red-400" />
              </button>
            </div>
            <input
              type="text"
              placeholder="Degree"
              value={edu.degree}
              onChange={(e) => updateEducation(index, 'degree', e.target.value)}
              className={inputClass}
            />
            <input
              type="text"
              placeholder="Institution"
              value={edu.institution}
              onChange={(e) => updateEducation(index, 'institution', e.target.value)}
              className={inputClass}
            />
            <input
              type="text"
              placeholder="Year"
              value={edu.year}
              onChange={(e) => updateEducation(index, 'year', e.target.value)}
              className={inputClass}
            />
            <input
              type="text"
              placeholder="Grade/CGPA"
              value={edu.grade}
              onChange={(e) => updateEducation(index, 'grade', e.target.value)}
              className={inputClass}
            />
          </div>
        ))}
        <button
          onClick={addEducation}
          className="w-full p-2 bg-[#0f0f1a] border border-gray-700 rounded-lg hover:border-[#00cccc] transition-colors flex items-center justify-center space-x-2 text-[#00cccc]"
        >
          <Plus size={18} />
          <span>Add Education</span>
        </button>
      </Section>

      {/* Projects */}
      <Section title="Projects" sectionKey="projects" expandedSections={expandedSections} toggleSection={toggleSection}>
        {resumeData.projects.map((project, index) => (
          <div key={project.id || `project-${index}`} className="bg-[#0f0f1a] border border-gray-700 rounded-lg p-4 space-y-3">
            <div className="flex justify-between items-start">
              <h4 className="text-white font-medium">Project {index + 1}</h4>
              <button
                onClick={() => removeProject(index)}
                className="p-1 hover:bg-red-500/20 rounded transition-colors"
              >
                <Trash2 size={16} className="text-red-400" />
              </button>
            </div>
            <input
              type="text"
              placeholder="Project Title"
              value={project.title}
              onChange={(e) => updateProject(index, 'title', e.target.value)}
              className={inputClass}
            />
            <input
              type="text"
              placeholder="Tech Stack (e.g., React, Node.js, MongoDB)"
              value={project.techStack}
              onChange={(e) => updateProject(index, 'techStack', e.target.value)}
              className={inputClass}
            />
            <textarea
              placeholder="Project Description"
              value={project.description}
              onChange={(e) => updateProject(index, 'description', e.target.value)}
              rows="3"
              className={textareaClass}
            />
          </div>
        ))}
        <button
          onClick={addProject}
          className="w-full p-2 bg-[#0f0f1a] border border-gray-700 rounded-lg hover:border-[#00cccc] transition-colors flex items-center justify-center space-x-2 text-[#00cccc]"
        >
          <Plus size={18} />
          <span>Add Project</span>
        </button>
      </Section>

      {/* Certifications */}
      <Section title="Certifications" sectionKey="certifications" expandedSections={expandedSections} toggleSection={toggleSection}>
        {resumeData.certifications.map((cert, index) => (
          <div key={cert.id || `cert-${index}`} className="flex gap-2">
            <input
              type="text"
              placeholder="Certification name"
              value={typeof cert === 'string' ? cert : cert.text}
              onChange={(e) => updateCertification(index, e.target.value)}
              className={inputClass}
            />
            <button
              onClick={() => removeCertification(index)}
              className="p-2 bg-[#0f0f1a] border border-gray-700 rounded-lg hover:bg-red-500/20 hover:border-red-500 transition-colors"
            >
              <Trash2 size={18} className="text-red-400" />
            </button>
          </div>
        ))}
        <button
          onClick={addCertification}
          className="w-full p-2 bg-[#0f0f1a] border border-gray-700 rounded-lg hover:border-[#00cccc] transition-colors flex items-center justify-center space-x-2 text-[#00cccc]"
        >
          <Plus size={18} />
          <span>Add Certification</span>
        </button>
      </Section>

      {/* Achievements */}
      <Section title="Achievements" sectionKey="achievements" expandedSections={expandedSections} toggleSection={toggleSection}>
        {resumeData.achievements.map((achievement, index) => (
          <div key={achievement.id || `achievement-${index}`} className="flex gap-2">
            <input
              type="text"
              placeholder="Achievement"
              value={typeof achievement === 'string' ? achievement : achievement.text}
              onChange={(e) => updateAchievement(index, e.target.value)}
              className={inputClass}
            />
            <button
              onClick={() => removeAchievement(index)}
              className="p-2 bg-[#0f0f1a] border border-gray-700 rounded-lg hover:bg-red-500/20 hover:border-red-500 transition-colors"
            >
              <Trash2 size={18} className="text-red-400" />
            </button>
          </div>
        ))}
        <button
          onClick={addAchievement}
          className="w-full p-2 bg-[#0f0f1a] border border-gray-700 rounded-lg hover:border-[#00cccc] transition-colors flex items-center justify-center space-x-2 text-[#00cccc]"
        >
          <Plus size={18} />
          <span>Add Achievement</span>
        </button>
      </Section>
    </div>
  );
};

export default ResumeForm;
