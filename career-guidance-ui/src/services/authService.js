/**
 * Authentication Service
 * Handles all API calls related to authentication
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Sign up a new user
 * @param {Object} userData - User registration data
 * @param {string} userData.name - Full name
 * @param {string} userData.email - Email address
 * @param {string} userData.password - Password
 * @param {string} userData.domain - Domain of interest
 * @returns {Promise<Object>} Response with success, token, and user data
 */
export const signupUser = async (userData) => {
  try {
    const response = await fetch(`${API_URL}/api/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: userData.name,
        email: userData.email,
        password: userData.password,
        domain: userData.domain,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Signup failed');
    }

    // Store token and user data if successful
    if (data.success && data.token) {
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
    }

    return data;
  } catch (error) {
    console.error('Signup error:', error);
    return {
      success: false,
      message: error.message || 'Network error. Please try again.',
    };
  }
};

/**
 * Log in an existing user
 * @param {Object} credentials - Login credentials
 * @param {string} credentials.email - Email address
 * @param {string} credentials.password - Password
 * @returns {Promise<Object>} Response with success, token, and user data
 */
export const loginUser = async (credentials) => {
  try {
    const response = await fetch(`${API_URL}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Login failed');
    }

    // Store token and user data if successful
    if (data.success && data.token) {
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
    }

    return data;
  } catch (error) {
    console.error('Login error:', error);
    return {
      success: false,
      message: error.message || 'Network error. Please try again.',
    };
  }
};

/**
 * Get user profile
 * @returns {Promise<Object>} User profile data
 */
export const getProfile = async () => {
  try {
    const token = localStorage.getItem('authToken');

    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/profile`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      // Handle 401 Unauthorized - token invalid or expired
      if (response.status === 401) {
        logout();
        throw new Error('Session expired. Please login again.');
      }
      throw new Error(data.message || 'Failed to fetch profile');
    }

    return data;
  } catch (error) {
    console.error('Get profile error:', error);
    return {
      success: false,
      message: error.message || 'Failed to fetch profile',
    };
  }
};

/**
 * Log out user
 * Clears all authentication data from localStorage
 */
export const logout = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');
};

/**
 * Check if user is authenticated
 * @returns {boolean} True if user has valid token
 */
export const isAuthenticated = () => {
  const token = localStorage.getItem('authToken');
  return !!token;
};

/**
 * Get stored user data
 * @returns {Object|null} User data or null if not found
 */
export const getStoredUser = () => {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    try {
      return JSON.parse(userStr);
    } catch (error) {
      console.error('Error parsing stored user data:', error);
      return null;
    }
  }
  return null;
};

/**
 * Get stored auth token
 * @returns {string|null} Auth token or null if not found
 */
export const getStoredToken = () => {
  return localStorage.getItem('authToken');
};

/**
 * Upload a profile picture for the current user
 * @param {File} file - Image file to upload
 * @returns {Promise<Object>} Response with success and profile_picture_url
 */
export const uploadProfilePicture = async (file) => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      console.error('No auth token for profile picture upload');
      return { success: false, message: 'Not authenticated' };
    }

    const formData = new FormData();
    formData.append('picture', file);

    console.log('Uploading profile picture...', file.name, file.size);

    const response = await fetch(`${API_URL}/api/upload/profile-picture`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      // Do NOT set Content-Type — browser sets it with boundary for multipart
      body: formData,
    });

    const data = await response.json();
    console.log('Upload response:', data);

    if (data.success) {
      // Update stored user with new profile picture
      const user = getStoredUser();
      if (user) {
        user.profile_picture = data.profile_picture_url;
        localStorage.setItem('user', JSON.stringify(user));
      }
    }
    return data;
  } catch (error) {
    console.error('Profile picture upload error:', error);
    return { success: false, message: error.message || 'Upload failed' };
  }
};
