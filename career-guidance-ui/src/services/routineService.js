/**
 * Routine Service
 * Handles all API calls for the Routine Build module
 */

import { getStoredToken } from './authService';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const authHeaders = () => {
    const token = getStoredToken();
    return {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };
};

/**
 * Generate a learning routine from uploaded analysis file
 */
export const generateRoutineFromFile = async (file, hoursPerWeek = 10) => {
    try {
        const token = getStoredToken();
        if (!token) throw new Error('Authentication required');

        // Get the target domain the user selected in the Analyze module
        const analyzeTargetDomain = localStorage.getItem('analyzeTargetDomain') || '';
        // Fallback to user's profile domain if analyze domain not found
        const storedUser = localStorage.getItem('user');
        const profileDomain = storedUser ? JSON.parse(storedUser)?.domain || '' : '';
        const userDomain = analyzeTargetDomain || profileDomain;

        const formData = new FormData();
        formData.append('file', file);
        formData.append('hoursPerWeek', String(hoursPerWeek));
        if (userDomain) formData.append('userDomain', userDomain);

        const response = await fetch(`${API_URL}/api/routine/generate`, {
            method: 'POST',
            headers: {
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
            },
            body: formData,
        });

        const result = await response.json();
        if (!response.ok) {
            if (response.status === 401) throw new Error('Session expired. Please login again.');
            throw new Error(result.message || 'Routine generation failed');
        }
        return result;
    } catch (error) {
        console.error('generateRoutineFromFile error:', error);
        return { success: false, message: error.message || 'Network error' };
    }
};

/**
 * Generate a learning routine from Analyze output
 */
export const buildRoutine = async (analyzeData, hoursPerWeek = 10) => {
    try {
        const token = getStoredToken();
        if (!token) throw new Error('Authentication required');

        const response = await fetch(`${API_URL}/api/routine-build`, {
            method: 'POST',
            headers: authHeaders(),
            body: JSON.stringify({
                analyzeData,
                availableHoursPerWeek: hoursPerWeek,
            }),
        });

        const result = await response.json();
        if (!response.ok) {
            if (response.status === 401) throw new Error('Session expired. Please login again.');
            throw new Error(result.message || 'Routine build failed');
        }
        return result;
    } catch (error) {
        console.error('buildRoutine error:', error);
        return { success: false, message: error.message || 'Network error' };
    }
};

/**
 * Update skill progress with new endpoint
 */
export const updateRoutineProgress = async (week, skill, completionPercentage, date, routineData) => {
    try {
        const token = getStoredToken();
        if (!token) throw new Error('Authentication required');

        const response = await fetch(`${API_URL}/api/routine/progress`, {
            method: 'POST',
            headers: authHeaders(),
            body: JSON.stringify({
                week,
                skill,
                completionPercentage,
                date,
                routineData
            }),
        });

        const result = await response.json();
        if (!response.ok) {
            if (response.status === 401) throw new Error('Session expired. Please login again.');
            throw new Error(result.message || 'Progress update failed');
        }
        return result;
    } catch (error) {
        console.error('updateRoutineProgress error:', error);
        return { success: false, message: error.message || 'Network error' };
    }
};

/**
 * Update skill progress (legacy - kept for compatibility)
 */
export const updateProgress = async (skill, completionPercentage, currentWeek = 1, routineData = null) => {
    try {
        const token = getStoredToken();
        if (!token) throw new Error('Authentication required');

        const response = await fetch(`${API_URL}/api/update-progress`, {
            method: 'POST',
            headers: authHeaders(),
            body: JSON.stringify({ skill, completionPercentage, currentWeek, routineData }),
        });

        const result = await response.json();
        if (!response.ok) {
            if (response.status === 401) throw new Error('Session expired. Please login again.');
            throw new Error(result.message || 'Progress update failed');
        }
        return result;
    } catch (error) {
        console.error('updateProgress error:', error);
        return { success: false, message: error.message || 'Network error' };
    }
};

/**
 * Get evolution data with graphs and metrics
 */
export const getRoutineEvolution = async (routineData = null) => {
    try {
        const token = getStoredToken();
        if (!token) throw new Error('Authentication required');

        // Use the new analytics endpoint
        const url = `${API_URL}/api/routine/evolution/analytics`;
        
        const response = await fetch(url, {
            method: 'GET',
            headers: authHeaders(),
        });

        const result = await response.json();
        if (!response.ok) {
            if (response.status === 401) throw new Error('Session expired. Please login again.');
            throw new Error(result.message || 'Evolution data fetch failed');
        }
        return result;
    } catch (error) {
        console.error('getRoutineEvolution error:', error);
        return { success: false, message: error.message || 'Network error' };
    }
};

/**
 * Get evolution data with snapshots (legacy - kept for compatibility)
 */
export const getEvolutionData = async ({ recordSnapshot = false, completion = 0, skillsDone = '' } = {}) => {
    try {
        const token = getStoredToken();
        if (!token) throw new Error('Authentication required');

        const params = new URLSearchParams();
        if (recordSnapshot) {
            params.set('snapshot', 'record');
            params.set('completion', String(completion));
            if (skillsDone) params.set('skills_done', skillsDone);
        }

        const url = `${API_URL}/api/evolution-data${params.toString() ? `?${params}` : ''}`;

        const response = await fetch(url, {
            method: 'GET',
            headers: authHeaders(),
        });

        const result = await response.json();
        if (!response.ok) {
            if (response.status === 401) throw new Error('Session expired. Please login again.');
            throw new Error(result.message || 'Evolution data fetch failed');
        }
        return result;
    } catch (error) {
        console.error('getEvolutionData error:', error);
        return { success: false, message: error.message || 'Network error' };
    }
};

/**
 * Chat with AI Mentor about routine
 */
export const routineChat = async (userQuestion, routineData = null, progressData = null) => {
    try {
        const token = getStoredToken();
        if (!token) throw new Error('Authentication required');

        const response = await fetch(`${API_URL}/api/routine/chat`, {
            method: 'POST',
            headers: authHeaders(),
            body: JSON.stringify({
                userQuestion,
                routineData,
                progressData
            }),
        });

        const result = await response.json();
        if (!response.ok) {
            if (response.status === 401) throw new Error('Session expired. Please login again.');
            throw new Error(result.message || 'Chat failed');
        }
        return result;
    } catch (error) {
        console.error('routineChat error:', error);
        return { 
            success: false, 
            response: 'Sorry, I could not process your question. Please try again.',
            message: error.message || 'Network error' 
        };
    }
};

/**
 * Chat with AI Mentor (legacy - kept for compatibility)
 */
export const mentorChat = async (message, routineData = null, progressData = null, currentWeek = 1) => {
    try {
        const token = getStoredToken();
        if (!token) throw new Error('Authentication required');

        const response = await fetch(`${API_URL}/api/routine-mentor-chat`, {
            method: 'POST',
            headers: authHeaders(),
            body: JSON.stringify({ message, routineData, progressData, currentWeek }),
        });

        const result = await response.json();
        if (!response.ok) {
            if (response.status === 401) throw new Error('Session expired. Please login again.');
            throw new Error(result.message || 'Mentor chat failed');
        }
        return result;
    } catch (error) {
        console.error('mentorChat error:', error);
        return { success: false, message: error.message || 'Network error' };
    }
};
