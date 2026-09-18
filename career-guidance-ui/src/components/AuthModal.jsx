import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import InputField from './InputField';
import SelectField from './SelectField';
import Button from './Button';
import { signupUser, loginUser, uploadProfilePicture, getStoredUser } from '../services/authService';

const AuthModal = ({ isOpen, onClose, onAuthSuccess }) => {
  const [activeTab, setActiveTab] = useState('login'); // 'login', 'signup', 'forgot', 'forgot_sent'
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [profilePicFile, setProfilePicFile] = useState(null);
  const [profilePicPreview, setProfilePicPreview] = useState(null);
  const [forgotEmail, setForgotEmail] = useState('');
  const [devResetLink, setDevResetLink] = useState('');
  const picInputRef = useRef(null);

  // Login form state
  const [loginData, setLoginData] = useState({
    email: '',
    password: '',
  });

  // Signup form state
  const [signupData, setSignupData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    domain: '',
    agreeToTerms: false,
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

  // Validation functions
  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const validateLoginForm = () => {
    const newErrors = {};

    if (!loginData.email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(loginData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!loginData.password) {
      newErrors.password = 'Password is required';
    } else if (loginData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validateSignupForm = () => {
    const newErrors = {};

    if (!signupData.fullName) {
      newErrors.fullName = 'Full name is required';
    }

    if (!signupData.email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(signupData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!signupData.password) {
      newErrors.password = 'Password is required';
    } else if (signupData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (!signupData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (signupData.password !== signupData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!signupData.domain) {
      newErrors.domain = 'Please select a domain of interest';
    }


    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    if (validateLoginForm()) {
      setIsLoading(true);
      setErrors({});

      try {
        const response = await loginUser({
          email: loginData.email,
          password: loginData.password,
        });

        if (response.success) {
          // Successful login — authService already stored full user in localStorage
          onAuthSuccess(getStoredUser() || response.user);
          resetForms();
          onClose();
        } else {
          // Login failed - show error
          setErrors({ general: response.message || 'Login failed. Please try again.' });
        }
      } catch (error) {
        setErrors({ general: 'Network error. Please check your connection.' });
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    if (validateSignupForm()) {
      setIsLoading(true);
      setErrors({});

      try {
        const response = await signupUser({
          name: signupData.fullName,
          email: signupData.email,
          password: signupData.password,
          domain: signupData.domain,
        });

        if (response.success) {
          // Upload profile picture if one was selected (token is now stored)
          if (profilePicFile) {
            await uploadProfilePicture(profilePicFile);
          }
          // onAuthSuccess reads the full stored user (with profile_picture already updated)
          onAuthSuccess(getStoredUser() || response.user);
          resetForms();
          onClose();
        } else {
          setErrors({ general: response.message || 'Signup failed. Please try again.' });
        }
      } catch (error) {
        setErrors({ general: 'Network error. Please check your connection.' });
      } finally {
        setIsLoading(false);
      }
    }
  };

  const resetForms = () => {
    setLoginData({ email: '', password: '' });
    setSignupData({
      fullName: '',
      email: '',
      password: '',
      confirmPassword: '',
      domain: '',
      agreeToTerms: false,
    });
    setErrors({});
    setProfilePicFile(null);
    setProfilePicPreview(null);
    setForgotEmail('');
    setDevResetLink('');
  };

  const handleForgotSubmit = async (e) => {
    e.preventDefault();
    if (!forgotEmail) { setErrors({ forgotEmail: 'Email is required' }); return; }
    setIsLoading(true);
    setErrors({});
    try {
      const res = await fetch('http://localhost:5000/api/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: forgotEmail })
      });
      const data = await res.json();
      if (data.success) {
        if (data.dev_reset_link) setDevResetLink(data.dev_reset_link);
        setActiveTab('forgot_sent');
      } else {
        setErrors({ forgotEmail: data.message || 'Something went wrong' });
      }
    } catch {
      setErrors({ forgotEmail: 'Network error. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handlePicChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setProfilePicFile(file);
    setProfilePicPreview(URL.createObjectURL(file));
  };

  const handleClose = () => {
    resetForms();
    onClose();
  };

  const switchTab = (tab) => {
    setActiveTab(tab);
    setErrors({});
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <div className="fixed inset-0 flex items-center justify-center z-50 p-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              transition={{ type: 'spring', duration: 0.5 }}
              className="glass rounded-2xl w-full max-w-md max-h-[90vh] overflow-y-auto relative glow-violet"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Close Button */}
              <button
                onClick={handleClose}
                className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors z-10"
              >
                <X size={24} />
              </button>

              {/* Modal Content */}
              <div className="p-8">
                {/* Header */}
                <div className="text-center mb-6">
                  <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-2">
                    Welcome to CareerAI
                  </h2>
                  <p className="text-gray-400 text-sm">
                    Your intelligent career guidance companion
                  </p>
                </div>

                {/* Tab Switcher */}
                {activeTab !== 'forgot' && activeTab !== 'forgot_sent' && (
                <div className="flex gap-2 mb-6 p-1 glass rounded-lg">
                  <button
                    onClick={() => switchTab('login')}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all duration-300 ${
                      activeTab === 'login'
                        ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                        : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    Login
                  </button>
                  <button
                    onClick={() => switchTab('signup')}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all duration-300 ${
                      activeTab === 'signup'
                        ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                        : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    Sign Up
                  </button>
                </div>
                )}

                {/* Forms */}
                <AnimatePresence mode="wait">
                  {activeTab === 'forgot' ? (
                    <motion.form
                      key="forgot"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      transition={{ duration: 0.3 }}
                      onSubmit={handleForgotSubmit}
                      className="space-y-4"
                    >
                      <p className="text-gray-400 text-sm">Enter your account email and we'll send you a reset link.</p>
                      <InputField
                        label="Email"
                        type="email"
                        name="forgotEmail"
                        value={forgotEmail}
                        onChange={(e) => setForgotEmail(e.target.value)}
                        error={errors.forgotEmail}
                        placeholder="your@email.com"
                        required
                      />
                      {errors.forgotEmail && (
                        <p className="text-red-400 text-xs">{errors.forgotEmail}</p>
                      )}
                      <Button type="submit" variant="primary" className="w-full" disabled={isLoading}>
                        {isLoading ? 'Sending...' : 'Send Reset Link'}
                      </Button>
                      <button
                        type="button"
                        onClick={() => switchTab('login')}
                        className="w-full text-center text-gray-400 hover:text-white text-sm mt-2"
                      >
                        ← Back to Login
                      </button>
                    </motion.form>
                  ) : activeTab === 'forgot_sent' ? (
                    <motion.div
                      key="forgot_sent"
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className="text-center space-y-4 py-4"
                    >
                      <div className="text-5xl">📧</div>
                      <h3 className="text-white font-bold text-lg">Check your inbox</h3>
                      <p className="text-gray-400 text-sm">
                        If <span className="text-purple-400">{forgotEmail}</span> is registered, a reset link has been sent. It expires in 15 minutes.
                      </p>
                      {devResetLink && (
                        <div className="bg-yellow-500/10 border border-yellow-500/40 rounded-lg p-3 text-left">
                          <p className="text-yellow-400 text-xs font-semibold mb-1">⚠ Email not configured — use this link to reset:</p>
                          <a
                            href={devResetLink}
                            className="text-purple-400 text-xs break-all underline hover:text-purple-300"
                          >
                            {devResetLink}
                          </a>
                        </div>
                      )}
                      <button
                        type="button"
                        onClick={() => switchTab('login')}
                        className="w-full py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-medium mt-4"
                      >
                        Back to Login
                      </button>
                    </motion.div>
                  ) : activeTab === 'login' ? (
                    <motion.form
                      key="login"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      transition={{ duration: 0.3 }}
                      onSubmit={handleLoginSubmit}
                      className="space-y-4"
                    >
                      <InputField
                        label="Email"
                        type="email"
                        name="email"
                        value={loginData.email}
                        onChange={(e) =>
                          setLoginData({ ...loginData, email: e.target.value })
                        }
                        error={errors.email}
                        placeholder="your@email.com"
                        required
                      />

                      <InputField
                        label="Password"
                        type="password"
                        name="password"
                        value={loginData.password}
                        onChange={(e) =>
                          setLoginData({ ...loginData, password: e.target.value })
                        }
                        error={errors.password}
                        placeholder="••••••••"
                        required
                      />

                      <div className="flex items-center justify-between text-sm">
                        <label className="flex items-center text-gray-400">
                          <input
                            type="checkbox"
                            className="mr-2 rounded border-gray-600 bg-white/5"
                          />
                          Remember me
                        </label>
                        <a
                          href="#"
                          onClick={(e) => { e.preventDefault(); switchTab('forgot'); }}
                          className="text-purple-400 hover:text-purple-300"
                        >
                          Forgot password?
                        </a>
                      </div>

                      {errors.general && (
                        <motion.div
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className="p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm"
                        >
                          {errors.general}
                        </motion.div>
                      )}

                      <Button
                        type="submit"
                        variant="primary"
                        className="w-full mt-6"
                        disabled={isLoading}
                      >
                        {isLoading ? 'Logging in...' : 'Login'}
                      </Button>
                    </motion.form>
                  ) : (
                    <motion.form
                      key="signup"
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -20 }}
                      transition={{ duration: 0.3 }}
                      onSubmit={handleSignupSubmit}
                      className="space-y-4"
                    >
                      {/* Profile Picture Picker */}
                      <div className="flex flex-col items-center gap-2 mb-2">
                        <div
                          onClick={() => picInputRef.current?.click()}
                          className="w-20 h-20 rounded-full border-2 border-dashed border-purple-500 flex items-center justify-center cursor-pointer overflow-hidden hover:border-purple-300 transition"
                          title="Click to upload profile picture"
                        >
                          {profilePicPreview ? (
                            <img src={profilePicPreview} alt="Preview" className="w-full h-full object-cover" />
                          ) : (
                            <span className="text-gray-400 text-xs text-center px-1">Add Photo</span>
                          )}
                        </div>
                        <input
                          ref={picInputRef}
                          type="file"
                          accept="image/png,image/jpeg,image/gif,image/webp"
                          className="hidden"
                          onChange={handlePicChange}
                        />
                        <p className="text-gray-500 text-xs">Optional profile picture</p>
                      </div>

                      <InputField
                        label="Full Name"
                        type="text"
                        name="fullName"
                        value={signupData.fullName}
                        onChange={(e) =>
                          setSignupData({ ...signupData, fullName: e.target.value })
                        }
                        error={errors.fullName}
                        placeholder="John Doe"
                        required
                      />

                      <InputField
                        label="Email"
                        type="email"
                        name="email"
                        value={signupData.email}
                        onChange={(e) =>
                          setSignupData({ ...signupData, email: e.target.value })
                        }
                        error={errors.email}
                        placeholder="your@email.com"
                        required
                      />

                      <InputField
                        label="Password"
                        type="password"
                        name="password"
                        value={signupData.password}
                        onChange={(e) =>
                          setSignupData({ ...signupData, password: e.target.value })
                        }
                        error={errors.password}
                        placeholder="••••••••"
                        required
                      />

                      <InputField
                        label="Confirm Password"
                        type="password"
                        name="confirmPassword"
                        value={signupData.confirmPassword}
                        onChange={(e) =>
                          setSignupData({
                            ...signupData,
                            confirmPassword: e.target.value,
                          })
                        }
                        error={errors.confirmPassword}
                        placeholder="••••••••"
                        required
                      />

                      <SelectField
                        label="Domain of Interest"
                        name="domain"
                        value={signupData.domain}
                        onChange={(e) =>
                          setSignupData({ ...signupData, domain: e.target.value })
                        }
                        options={domains}
                        error={errors.domain}
                        required
                      />


                      {errors.general && (
                        <motion.div
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className="p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm"
                        >
                          {errors.general}
                        </motion.div>
                      )}

                      <Button
                        type="submit"
                        variant="primary"
                        className="w-full mt-6"
                        disabled={isLoading}
                      >
                        {isLoading ? 'Signing up...' : 'Sign Up'}
                      </Button>
                    </motion.form>
                  )}
                </AnimatePresence>

                {/* Social Login (Optional) */}
                <div className="mt-6">
                  <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                      <div className="w-full border-t border-gray-700"></div>
                    </div>
                    <div className="relative flex justify-center text-sm">
                      <span className="px-2 bg-transparent text-gray-500">
                        Or continue with
                      </span>
                    </div>
                  </div>

                  <div className="mt-4 grid grid-cols-2 gap-3">
                    <button
                      type="button"
                      className="glass px-4 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:glow-violet transition-all duration-300"
                    >
                      Google
                    </button>
                    <button
                      type="button"
                      className="glass px-4 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:glow-violet transition-all duration-300"
                    >
                      GitHub
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
};

export default AuthModal;
