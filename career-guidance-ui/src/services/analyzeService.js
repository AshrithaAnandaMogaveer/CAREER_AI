/**
 * Analyze Service
 * Handles all API calls related to career analysis
 */

import { getStoredToken } from './authService';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Comprehensive resume analysis with NLP and PDF generation
 * @param {Object} data - Analysis data
 * @param {File} data.file - Resume file (optional)
 * @param {string} data.currentDomain - Current domain
 * @param {string} data.targetDomain - Target domain
 * @param {number} data.experienceYears - Years of experience
 * @param {string} data.manualSkills - Manual skills input
 * @param {string} data.projectDescriptions - Project descriptions
 * @param {string} data.certifications - Certifications
 * @param {string} data.strengthLevel - Strength level
 * @returns {Promise<Object>} Comprehensive analysis results
 */
export const analyzeResumeComprehensive = async (data) => {
  try {
    const token = getStoredToken();
    
    if (!token) {
      throw new Error('Authentication required');
    }

    const formData = new FormData();
    
    // Add file if provided
    if (data.file) {
      formData.append('resume', data.file);
    }
    
    // Add all form fields
    formData.append('currentDomain', data.currentDomain || '');
    formData.append('targetDomain', data.targetDomain || 'Software Development');
    formData.append('experienceYears', data.experienceYears || '0');
    formData.append('manualSkills', data.manualSkills || '');
    formData.append('projectDescriptions', data.projectDescriptions || '');
    formData.append('certifications', data.certifications || '');
    formData.append('strengthLevel', data.strengthLevel || 'Intermediate');

    const response = await fetch(`${API_URL}/api/analyze-resume`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });

    const result = await response.json();

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Session expired. Please login again.');
      }
      throw new Error(result.message || 'Analysis failed');
    }

    return result;
  } catch (error) {
    console.error('Comprehensive analysis error:', error);
    return {
      success: false,
      message: error.message || 'Network error. Please try again.',
    };
  }
};

/**
 * Upload resume for analysis (Legacy - redirects to comprehensive)
 * @param {File} file - Resume file (PDF/DOC)
 * @returns {Promise<Object>} Analysis results
 */
export const uploadResume = async (file) => {
  return analyzeResumeComprehensive({ file });
};

/**
 * Analyze manually entered skills (Legacy - redirects to comprehensive)
 * @param {Object} data - Manual input data
 * @param {string} data.skills - Skills text
 * @param {string} data.domain - Selected domain
 * @returns {Promise<Object>} Analysis results
 */
export const analyzeManualInput = async (data) => {
  return analyzeResumeComprehensive({
    manualSkills: data.skills,
    targetDomain: data.domain,
  });
};
