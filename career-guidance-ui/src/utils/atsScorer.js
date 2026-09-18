/**
 * ATS Score Calculator
 * Calculates resume ATS-friendliness score out of 100
 */

export const calculateATSScore = (resumeData) => {
  let score = 0;
  const breakdown = {};

  // 1. Professional Summary (10 points)
  if (resumeData.summary && resumeData.summary.trim().length > 50) {
    score += 10;
    breakdown.summary = 10;
  } else if (resumeData.summary && resumeData.summary.trim().length > 0) {
    score += 5;
    breakdown.summary = 5;
  } else {
    breakdown.summary = 0;
  }

  // 2. Skills Count (15 points)
  const skillsCount = resumeData.skills.filter(s => {
    const skillText = typeof s === 'string' ? s : s?.text;
    return skillText && skillText.trim();
  }).length;
  if (skillsCount >= 10) {
    score += 15;
    breakdown.skills = 15;
  } else if (skillsCount >= 5) {
    score += 10;
    breakdown.skills = 10;
  } else if (skillsCount > 0) {
    score += 5;
    breakdown.skills = 5;
  } else {
    breakdown.skills = 0;
  }

  // 3. Experience (20 points)
  const experienceCount = resumeData.experience.filter(
    exp => exp.role && exp.company
  ).length;
  if (experienceCount >= 3) {
    score += 20;
    breakdown.experience = 20;
  } else if (experienceCount >= 2) {
    score += 15;
    breakdown.experience = 15;
  } else if (experienceCount >= 1) {
    score += 10;
    breakdown.experience = 10;
  } else {
    breakdown.experience = 0;
  }

  // 4. Projects (15 points)
  const projectsCount = resumeData.projects.filter(
    proj => proj.title && proj.description
  ).length;
  if (projectsCount >= 3) {
    score += 15;
    breakdown.projects = 15;
  } else if (projectsCount >= 2) {
    score += 10;
    breakdown.projects = 10;
  } else if (projectsCount >= 1) {
    score += 5;
    breakdown.projects = 5;
  } else {
    breakdown.projects = 0;
  }

  // 5. Certifications (10 points)
  const certsCount = resumeData.certifications.filter(c => {
    const certText = typeof c === 'string' ? c : c?.text;
    return certText && certText.trim();
  }).length;
  if (certsCount >= 3) {
    score += 10;
    breakdown.certifications = 10;
  } else if (certsCount >= 1) {
    score += 5;
    breakdown.certifications = 5;
  } else {
    breakdown.certifications = 0;
  }

  // 6. Contact Info Completeness (10 points)
  const contactFields = ['name', 'email', 'phone', 'location'];
  const filledContacts = contactFields.filter(
    field => resumeData.personalInfo[field] && resumeData.personalInfo[field].trim()
  ).length;
  score += Math.floor((filledContacts / contactFields.length) * 10);
  breakdown.contactInfo = Math.floor((filledContacts / contactFields.length) * 10);

  // 7. Keyword Density (20 points - placeholder for future enhancement)
  // Basic check: presence of action verbs and technical terms
  const allText = [
    resumeData.summary,
    ...resumeData.skills.map(s => typeof s === 'string' ? s : s?.text || ''),
    ...resumeData.experience.map(e => e.description),
    ...resumeData.projects.map(p => p.description),
  ].join(' ').toLowerCase();

  const actionVerbs = ['developed', 'managed', 'led', 'created', 'implemented', 'designed', 'built', 'improved', 'achieved', 'delivered'];
  const verbsFound = actionVerbs.filter(verb => allText.includes(verb)).length;
  
  if (verbsFound >= 5) {
    score += 20;
    breakdown.keywords = 20;
  } else if (verbsFound >= 3) {
    score += 15;
    breakdown.keywords = 15;
  } else if (verbsFound >= 1) {
    score += 10;
    breakdown.keywords = 10;
  } else {
    breakdown.keywords = 0;
  }

  return {
    score: Math.min(score, 100),
    breakdown,
    recommendations: generateRecommendations(score, breakdown),
  };
};

const generateRecommendations = (score, breakdown) => {
  const recommendations = [];

  if (breakdown.summary < 10) {
    recommendations.push('Add a professional summary (50+ characters)');
  }
  if (breakdown.skills < 10) {
    recommendations.push('Add at least 5 relevant skills');
  }
  if (breakdown.experience < 15) {
    recommendations.push('Add more work experience entries');
  }
  if (breakdown.projects < 10) {
    recommendations.push('Include 2-3 projects with descriptions');
  }
  if (breakdown.certifications < 5) {
    recommendations.push('Add relevant certifications');
  }
  if (breakdown.contactInfo < 10) {
    recommendations.push('Complete all contact information fields');
  }
  if (breakdown.keywords < 15) {
    recommendations.push('Use more action verbs (developed, managed, led, etc.)');
  }

  return recommendations;
};

export const getScoreColor = (score) => {
  if (score >= 76) return { color: '#10b981', label: 'Excellent' }; // Green
  if (score >= 51) return { color: '#f59e0b', label: 'Good' }; // Yellow
  return { color: '#ef4444', label: 'Needs Work' }; // Red
};

export const getScoreGradient = (score) => {
  if (score >= 76) return 'from-green-500 to-emerald-500';
  if (score >= 51) return 'from-yellow-500 to-orange-500';
  return 'from-red-500 to-rose-500';
};
