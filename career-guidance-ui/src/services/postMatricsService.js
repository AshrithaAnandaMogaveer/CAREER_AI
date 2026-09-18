import { calculateAfter10thResults } from '../utils/after10thScoring';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Mock data fallback flag
const USE_MOCK_DATA = true; // Set to false when backend is ready

// After 10th Guidance - Dynamic Algorithm-Based
export const getAfter10thResult = async (data) => {
  try {
    // Use local algorithm for now
    const results = calculateAfter10thResults(data);
    
    return {
      success: true,
      streams: results,
    };

    /* 
    // Future backend integration:
    const response = await fetch(`${API_BASE_URL}/postmatrics/after10th`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch recommendations');
    }

    return await response.json();
    */
  } catch (error) {
    console.error('Error in After 10th guidance:', error);
    throw error;
  }
};

// After 10th Guidance (Legacy - kept for compatibility)
export const getAfter10thRecommendations = async (data) => {
  if (USE_MOCK_DATA) {
    // Return mock data for development
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          recommendations: [
            {
              stream: 'science',
              score: 85,
              name: 'Science (PCM/PCB)',
              description: 'Ideal for engineering, medicine, and research careers',
            },
          ],
        });
      }, 500);
    });
  }

  try {
    const response = await fetch(`${API_BASE_URL}/postmatrics/after10th`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch recommendations');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching after 10th recommendations:', error);
    throw error;
  }
};

// After 12th Guidance
export const getAfter12thRecommendations = async (data) => {
  if (USE_MOCK_DATA) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          recommendations: [
            {
              name: 'B.Tech/B.E.',
              feasibilityScore: 90,
              duration: '4 years',
              avgCost: 400000,
            },
          ],
        });
      }, 500);
    });
  }

  try {
    const response = await fetch(`${API_BASE_URL}/postmatrics/after12th`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch recommendations');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching after 12th recommendations:', error);
    throw error;
  }
};

// Competitive Exams
export const getCompetitiveExams = async (data) => {
  if (USE_MOCK_DATA) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          exams: [
            {
              name: 'JEE Main',
              matchScore: 85,
              difficulty: 'high',
              prepTime: 18,
            },
          ],
        });
      }, 500);
    });
  }

  try {
    const response = await fetch(`${API_BASE_URL}/postmatrics/exams`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch exams');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching competitive exams:', error);
    throw error;
  }
};

// Skill-Based Careers
export const getSkillBasedCareers = async (data) => {
  if (USE_MOCK_DATA) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          careers: [
            {
              name: 'Web Development',
              accessibilityScore: 90,
              avgIncome: 40000,
              learningTime: '6-12 months',
            },
          ],
        });
      }, 500);
    });
  }

  try {
    const response = await fetch(`${API_BASE_URL}/postmatrics/skills`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch careers');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching skill-based careers:', error);
    throw error;
  }
};

// Scholarships
export const getScholarships = async (data) => {
  if (USE_MOCK_DATA) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          scholarships: [
            {
              name: 'National Merit Scholarship',
              amount: 50000,
              provider: 'Central Government',
            },
          ],
        });
      }, 500);
    });
  }

  try {
    const response = await fetch(`${API_BASE_URL}/postmatrics/scholarships`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch scholarships');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching scholarships:', error);
    throw error;
  }
};

// Interest Assessment Test
export const submitInterestTest = async (answers) => {
  if (USE_MOCK_DATA) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          results: [
            {
              cluster: 'analytical',
              score: 85,
              name: 'Analytical & Scientific',
            },
          ],
        });
      }, 500);
    });
  }

  try {
    const response = await fetch(`${API_BASE_URL}/postmatrics/interest-test`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ answers }),
    });

    if (!response.ok) {
      throw new Error('Failed to submit test');
    }

    return await response.json();
  } catch (error) {
    console.error('Error submitting interest test:', error);
    throw error;
  }
};

export default {
  getAfter10thRecommendations,
  getAfter12thRecommendations,
  getCompetitiveExams,
  getSkillBasedCareers,
  getScholarships,
  submitInterestTest,
};
