const ResumePreview = ({ resumeData, template, previewMode = false, previewTheme = 'light' }) => {
  const renderTemplate = () => {
    switch (template) {
      case 'modern':
        return <ModernTemplate data={resumeData} theme={previewTheme} />;
      case 'minimal':
        return <MinimalTemplate data={resumeData} theme={previewTheme} />;
      case 'executive':
        return <ExecutiveTemplate data={resumeData} theme={previewTheme} />;
      case 'fresher':
        return <FresherTemplate data={resumeData} theme={previewTheme} />;
      case 'technical':
        return <TechnicalTemplate data={resumeData} theme={previewTheme} />;
      default:
        return <ModernTemplate data={resumeData} theme={previewTheme} />;
    }
  };

  const bgColor = previewTheme === 'dark' ? 'bg-slate-900' : 'bg-white';
  const textColor = previewTheme === 'dark' ? 'text-white' : 'text-black';

  return (
    <div>
      <div
        className={`${bgColor} ${textColor} rounded-lg shadow-2xl p-8 relative`}
        style={{ fontFamily: 'Arial, sans-serif', minHeight: '800px' }}
        data-resume-preview
      >
        {/* Watermark Overlay - Only visible in preview mode */}
        {previewMode && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none overflow-hidden">
            <div 
              className="text-gray-400/5 font-bold select-none"
              style={{
                fontSize: '120px',
                transform: 'rotate(-30deg)',
                whiteSpace: 'nowrap',
              }}
            >
              PREVIEW MODE
            </div>
          </div>
        )}
        
        {/* Resume Content */}
        <div className="relative z-10">
          {renderTemplate()}
        </div>
      </div>
    </div>
  );
};

// Modern Professional Template
const ModernTemplate = ({ data, theme = 'light' }) => {
  const isDark = theme === 'dark';
  const textPrimary = isDark ? 'text-white' : 'text-gray-900';
  const textSecondary = isDark ? 'text-gray-300' : 'text-gray-700';
  const textTertiary = isDark ? 'text-gray-400' : 'text-gray-600';
  const borderColor = isDark ? 'border-gray-700' : 'border-blue-600';
  const bgAccent = isDark ? 'bg-blue-900/30' : 'bg-blue-100';
  const textAccent = isDark ? 'text-blue-400' : 'text-blue-800';
  
  return (
    <div className="space-y-4">
      {/* Header */}
      <div className={`border-b-2 ${borderColor} pb-4`}>
        <h1 className={`text-3xl font-bold ${textPrimary}`}>{data.personalInfo.name || 'Your Name'}</h1>
        <div className={`flex flex-wrap gap-3 mt-2 text-sm ${textTertiary}`}>
          {data.personalInfo.email && <span>{data.personalInfo.email}</span>}
          {data.personalInfo.phone && <span>• {data.personalInfo.phone}</span>}
          {data.personalInfo.location && <span>• {data.personalInfo.location}</span>}
        </div>
        <div className={`flex flex-wrap gap-3 mt-1 text-sm ${isDark ? 'text-blue-400' : 'text-blue-600'}`}>
          {data.personalInfo.linkedin && <span>{data.personalInfo.linkedin}</span>}
          {data.personalInfo.github && <span>• {data.personalInfo.github}</span>}
        </div>
      </div>

      {/* Summary */}
      {data.summary && (
        <div>
          <h2 className={`text-xl font-bold ${textPrimary} mb-2`}>PROFESSIONAL SUMMARY</h2>
          <p className={`text-sm ${textSecondary} leading-relaxed`}>{data.summary}</p>
        </div>
      )}

      {/* Skills */}
      {data.skills.length > 0 && (
        <div>
          <h2 className={`text-xl font-bold ${textPrimary} mb-2`}>SKILLS</h2>
          <div className="flex flex-wrap gap-2">
            {data.skills.map((skill, index) => {
              const skillText = typeof skill === 'string' ? skill : skill.text;
              return skillText && <span key={index} className={`px-3 py-1 ${bgAccent} ${textAccent} rounded text-sm`}>{skillText}</span>
            })}
          </div>
        </div>
      )}

      {/* Experience */}
      {data.experience.length > 0 && (
        <div>
          <h2 className={`text-xl font-bold ${textPrimary} mb-2`}>EXPERIENCE</h2>
          {data.experience.map((exp, index) => (
            <div key={index} className="mb-3">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className={`font-bold ${textPrimary}`}>{exp.role || 'Role'}</h3>
                  <p className={`text-sm ${textSecondary}`}>{exp.company || 'Company'}</p>
                </div>
                <span className={`text-sm ${textTertiary}`}>{exp.duration}</span>
              </div>
              {exp.description && <p className={`text-sm ${textSecondary} mt-1`}>{exp.description}</p>}
            </div>
          ))}
        </div>
      )}

      {/* Education */}
      {data.education.length > 0 && (
        <div>
          <h2 className={`text-xl font-bold ${textPrimary} mb-2`}>EDUCATION</h2>
          {data.education.map((edu, index) => (
            <div key={index} className="mb-2">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className={`font-bold ${textPrimary}`}>{edu.degree || 'Degree'}</h3>
                  <p className={`text-sm ${textSecondary}`}>{edu.institution || 'Institution'}</p>
                </div>
                <div className="text-right">
                  <span className={`text-sm ${textTertiary}`}>{edu.year}</span>
                  {edu.grade && <p className={`text-sm ${textSecondary}`}>{edu.grade}</p>}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Projects */}
      {data.projects.length > 0 && (
        <div>
          <h2 className={`text-xl font-bold ${textPrimary} mb-2`}>PROJECTS</h2>
          {data.projects.map((project, index) => (
            <div key={index} className="mb-3">
              <h3 className={`font-bold ${textPrimary}`}>{project.title || 'Project Title'}</h3>
              {project.techStack && <p className={`text-sm ${isDark ? 'text-blue-400' : 'text-blue-600'} italic`}>{project.techStack}</p>}
              {project.description && <p className={`text-sm ${textSecondary} mt-1`}>{project.description}</p>}
            </div>
          ))}
        </div>
      )}

      {/* Certifications */}
      {data.certifications.length > 0 && (
        <div>
          <h2 className={`text-xl font-bold ${textPrimary} mb-2`}>CERTIFICATIONS</h2>
          <ul className="list-disc list-inside space-y-1">
            {data.certifications.map((cert, index) => {
              const certText = typeof cert === 'string' ? cert : cert.text;
              return certText && <li key={index} className={`text-sm ${textSecondary}`}>{certText}</li>
            })}
          </ul>
        </div>
      )}

      {/* Achievements */}
      {data.achievements.length > 0 && (
        <div>
          <h2 className={`text-xl font-bold ${textPrimary} mb-2`}>ACHIEVEMENTS</h2>
          <ul className="list-disc list-inside space-y-1">
            {data.achievements.map((achievement, index) => {
              const achievementText = typeof achievement === 'string' ? achievement : achievement.text;
              return achievementText && <li key={index} className={`text-sm ${textSecondary}`}>{achievementText}</li>
            })}
          </ul>
        </div>
      )}
    </div>
  );
};

// Minimal Clean Template
const MinimalTemplate = ({ data }) => (
  <div className="space-y-5">
    <div className="text-center pb-4 border-b border-gray-300">
      <h1 className="text-4xl font-light text-gray-900">{data.personalInfo.name || 'Your Name'}</h1>
      <div className="flex justify-center flex-wrap gap-2 mt-2 text-xs text-gray-600">
        {data.personalInfo.email && <span>{data.personalInfo.email}</span>}
        {data.personalInfo.phone && <span>| {data.personalInfo.phone}</span>}
        {data.personalInfo.location && <span>| {data.personalInfo.location}</span>}
      </div>
    </div>

    {data.summary && (
      <div>
        <h2 className="text-sm font-bold text-gray-900 uppercase tracking-wide mb-2">Summary</h2>
        <p className="text-sm text-gray-700">{data.summary}</p>
      </div>
    )}

    {data.skills.length > 0 && (
      <div>
        <h2 className="text-sm font-bold text-gray-900 uppercase tracking-wide mb-2">Skills</h2>
        <p className="text-sm text-gray-700">{data.skills.map(s => typeof s === 'string' ? s : s.text).filter(s => s).join(' • ')}</p>
      </div>
    )}

    {data.experience.length > 0 && (
      <div>
        <h2 className="text-sm font-bold text-gray-900 uppercase tracking-wide mb-2">Experience</h2>
        {data.experience.map((exp, index) => (
          <div key={index} className="mb-3">
            <div className="flex justify-between">
              <h3 className="font-semibold text-gray-900 text-sm">{exp.role}</h3>
              <span className="text-xs text-gray-600">{exp.duration}</span>
            </div>
            <p className="text-xs text-gray-600 italic">{exp.company}</p>
            {exp.description && <p className="text-xs text-gray-700 mt-1">{exp.description}</p>}
          </div>
        ))}
      </div>
    )}

    {data.education.length > 0 && (
      <div>
        <h2 className="text-sm font-bold text-gray-900 uppercase tracking-wide mb-2">Education</h2>
        {data.education.map((edu, index) => (
          <div key={index} className="mb-2">
            <div className="flex justify-between">
              <h3 className="font-semibold text-gray-900 text-sm">{edu.degree}</h3>
              <span className="text-xs text-gray-600">{edu.year}</span>
            </div>
            <p className="text-xs text-gray-600">{edu.institution}</p>
          </div>
        ))}
      </div>
    )}
  </div>
);

// Executive Two-Column Template
const ExecutiveTemplate = ({ data }) => (
  <div className="grid grid-cols-3 gap-6">
    {/* Left Column */}
    <div className="col-span-1 space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{data.personalInfo.name || 'Your Name'}</h1>
      </div>

      <div className="text-xs text-gray-600 space-y-1">
        {data.personalInfo.email && <p>{data.personalInfo.email}</p>}
        {data.personalInfo.phone && <p>{data.personalInfo.phone}</p>}
        {data.personalInfo.location && <p>{data.personalInfo.location}</p>}
        {data.personalInfo.linkedin && <p className="text-blue-600">{data.personalInfo.linkedin}</p>}
      </div>

      {data.skills.length > 0 && (
        <div>
          <h2 className="text-sm font-bold text-gray-900 uppercase mb-2 border-b border-gray-300 pb-1">Skills</h2>
          <ul className="text-xs text-gray-700 space-y-1">
            {data.skills.map((skill, index) => {
              const skillText = typeof skill === 'string' ? skill : skill.text;
              return skillText && <li key={index}>• {skillText}</li>
            })}
          </ul>
        </div>
      )}

      {data.certifications.length > 0 && (
        <div>
          <h2 className="text-sm font-bold text-gray-900 uppercase mb-2 border-b border-gray-300 pb-1">Certifications</h2>
          <ul className="text-xs text-gray-700 space-y-1">
            {data.certifications.map((cert, index) => {
              const certText = typeof cert === 'string' ? cert : cert.text;
              return certText && <li key={index}>• {certText}</li>
            })}
          </ul>
        </div>
      )}
    </div>

    {/* Right Column */}
    <div className="col-span-2 space-y-4">
      {data.summary && (
        <div>
          <h2 className="text-sm font-bold text-gray-900 uppercase mb-2 border-b-2 border-gray-900 pb-1">Profile</h2>
          <p className="text-xs text-gray-700">{data.summary}</p>
        </div>
      )}

      {data.experience.length > 0 && (
        <div>
          <h2 className="text-sm font-bold text-gray-900 uppercase mb-2 border-b-2 border-gray-900 pb-1">Experience</h2>
          {data.experience.map((exp, index) => (
            <div key={index} className="mb-3">
              <div className="flex justify-between">
                <h3 className="font-bold text-gray-900 text-sm">{exp.role}</h3>
                <span className="text-xs text-gray-600">{exp.duration}</span>
              </div>
              <p className="text-xs text-gray-600 italic">{exp.company}</p>
              {exp.description && <p className="text-xs text-gray-700 mt-1">{exp.description}</p>}
            </div>
          ))}
        </div>
      )}

      {data.education.length > 0 && (
        <div>
          <h2 className="text-sm font-bold text-gray-900 uppercase mb-2 border-b-2 border-gray-900 pb-1">Education</h2>
          {data.education.map((edu, index) => (
            <div key={index} className="mb-2">
              <div className="flex justify-between">
                <h3 className="font-bold text-gray-900 text-sm">{edu.degree}</h3>
                <span className="text-xs text-gray-600">{edu.year}</span>
              </div>
              <p className="text-xs text-gray-600">{edu.institution}</p>
            </div>
          ))}
        </div>
      )}

      {data.projects.length > 0 && (
        <div>
          <h2 className="text-sm font-bold text-gray-900 uppercase mb-2 border-b-2 border-gray-900 pb-1">Projects</h2>
          {data.projects.map((project, index) => (
            <div key={index} className="mb-2">
              <h3 className="font-bold text-gray-900 text-sm">{project.title}</h3>
              {project.techStack && <p className="text-xs text-gray-600 italic">{project.techStack}</p>}
              {project.description && <p className="text-xs text-gray-700">{project.description}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  </div>
);

// Fresher Compact Template
const FresherTemplate = ({ data }) => (
  <div className="space-y-3">
    <div className="bg-gray-100 p-4 rounded">
      <h1 className="text-2xl font-bold text-gray-900">{data.personalInfo.name || 'Your Name'}</h1>
      <div className="text-xs text-gray-600 mt-1">
        {data.personalInfo.email} | {data.personalInfo.phone} | {data.personalInfo.location}
      </div>
    </div>

    {data.summary && (
      <div>
        <h2 className="text-sm font-bold text-gray-900 bg-gray-200 px-2 py-1">OBJECTIVE</h2>
        <p className="text-xs text-gray-700 mt-1 px-2">{data.summary}</p>
      </div>
    )}

    {data.education.length > 0 && (
      <div>
        <h2 className="text-sm font-bold text-gray-900 bg-gray-200 px-2 py-1">EDUCATION</h2>
        <div className="px-2 mt-1 space-y-2">
          {data.education.map((edu, index) => (
            <div key={index}>
              <div className="flex justify-between">
                <h3 className="font-semibold text-gray-900 text-xs">{edu.degree}</h3>
                <span className="text-xs text-gray-600">{edu.year}</span>
              </div>
              <p className="text-xs text-gray-600">{edu.institution}</p>
              {edu.grade && <p className="text-xs text-gray-600">Grade: {edu.grade}</p>}
            </div>
          ))}
        </div>
      </div>
    )}

    {data.skills.length > 0 && (
      <div>
        <h2 className="text-sm font-bold text-gray-900 bg-gray-200 px-2 py-1">SKILLS</h2>
        <p className="text-xs text-gray-700 mt-1 px-2">{data.skills.map(s => typeof s === 'string' ? s : s.text).filter(s => s).join(', ')}</p>
      </div>
    )}

    {data.projects.length > 0 && (
      <div>
        <h2 className="text-sm font-bold text-gray-900 bg-gray-200 px-2 py-1">PROJECTS</h2>
        <div className="px-2 mt-1 space-y-2">
          {data.projects.map((project, index) => (
            <div key={index}>
              <h3 className="font-semibold text-gray-900 text-xs">{project.title}</h3>
              {project.techStack && <p className="text-xs text-gray-600 italic">{project.techStack}</p>}
              {project.description && <p className="text-xs text-gray-700">{project.description}</p>}
            </div>
          ))}
        </div>
      </div>
    )}

    {data.certifications.length > 0 && (
      <div>
        <h2 className="text-sm font-bold text-gray-900 bg-gray-200 px-2 py-1">CERTIFICATIONS</h2>
        <ul className="text-xs text-gray-700 mt-1 px-2 space-y-1">
          {data.certifications.map((cert, index) => {
            const certText = typeof cert === 'string' ? cert : cert.text;
            return certText && <li key={index}>• {certText}</li>
          })}
        </ul>
      </div>
    )}
  </div>
);

// Technical Profile Template
const TechnicalTemplate = ({ data }) => (
  <div className="space-y-4">
    <div className="border-l-4 border-blue-600 pl-4">
      <h1 className="text-3xl font-bold text-gray-900">{data.personalInfo.name || 'Your Name'}</h1>
      <p className="text-sm text-gray-600 mt-1">
        {data.personalInfo.email} | {data.personalInfo.phone}
      </p>
      <p className="text-sm text-blue-600">
        {data.personalInfo.github} | {data.personalInfo.linkedin}
      </p>
    </div>

    {data.summary && (
      <div>
        <h2 className="text-lg font-bold text-gray-900 border-b-2 border-blue-600 pb-1">TECHNICAL PROFILE</h2>
        <p className="text-sm text-gray-700 mt-2">{data.summary}</p>
      </div>
    )}

    {data.skills.length > 0 && (
      <div>
        <h2 className="text-lg font-bold text-gray-900 border-b-2 border-blue-600 pb-1">TECHNICAL SKILLS</h2>
        <div className="mt-2 grid grid-cols-2 gap-2">
          {data.skills.map((skill, index) => {
            const skillText = typeof skill === 'string' ? skill : skill.text;
            return skillText && (
              <div key={index} className="text-sm text-gray-700">• {skillText}</div>
            )
          })}
        </div>
      </div>
    )}

    {data.experience.length > 0 && (
      <div>
        <h2 className="text-lg font-bold text-gray-900 border-b-2 border-blue-600 pb-1">PROFESSIONAL EXPERIENCE</h2>
        {data.experience.map((exp, index) => (
          <div key={index} className="mt-2">
            <div className="flex justify-between">
              <h3 className="font-bold text-gray-900">{exp.role}</h3>
              <span className="text-sm text-gray-600">{exp.duration}</span>
            </div>
            <p className="text-sm text-gray-600 italic">{exp.company}</p>
            {exp.description && <p className="text-sm text-gray-700 mt-1">{exp.description}</p>}
          </div>
        ))}
      </div>
    )}

    {data.projects.length > 0 && (
      <div>
        <h2 className="text-lg font-bold text-gray-900 border-b-2 border-blue-600 pb-1">TECHNICAL PROJECTS</h2>
        {data.projects.map((project, index) => (
          <div key={index} className="mt-2">
            <h3 className="font-bold text-gray-900">{project.title}</h3>
            {project.techStack && <p className="text-sm text-blue-600 italic">Tech Stack: {project.techStack}</p>}
            {project.description && <p className="text-sm text-gray-700">{project.description}</p>}
          </div>
        ))}
      </div>
    )}

    {data.education.length > 0 && (
      <div>
        <h2 className="text-lg font-bold text-gray-900 border-b-2 border-blue-600 pb-1">EDUCATION</h2>
        {data.education.map((edu, index) => (
          <div key={index} className="mt-2">
            <div className="flex justify-between">
              <h3 className="font-bold text-gray-900">{edu.degree}</h3>
              <span className="text-sm text-gray-600">{edu.year}</span>
            </div>
            <p className="text-sm text-gray-600">{edu.institution}</p>
          </div>
        ))}
      </div>
    )}
  </div>
);

export default ResumePreview;
