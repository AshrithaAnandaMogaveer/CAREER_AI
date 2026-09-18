import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import WhyUs from './components/WhyUs';
import HowItHelps from './components/HowItHelps';
import Footer from './components/Footer';
import AuthModal from './components/AuthModal';
import ProtectedRoute from './components/ProtectedRoute';
import Analyze from './pages/Analyze';
import Results from './pages/Results';
import CreateResume from './pages/CreateResume';
import BuildResume from './pages/BuildResume';
import PostMatrics from './pages/PostMatrics';
import RoutineBuild from './pages/RoutineBuild';
import Community from './pages/Community';
import Profile from './pages/Profile';
import Explore from './pages/Explore';
import ResetPassword from './pages/ResetPassword';
import { logout, isAuthenticated, getStoredUser } from './services/authService';

function App() {
  // Authentication state
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  // Check for existing authentication on component mount
  useEffect(() => {
    const checkAuth = () => {
      if (isAuthenticated()) {
        const storedUser = getStoredUser();
        if (storedUser) {
          setUser(storedUser);
          setIsLoggedIn(true);
          console.log('User session restored:', storedUser);
        }
      }
    };

    checkAuth();
  }, []);

  // Handle successful authentication
  const handleAuthSuccess = (userData) => {
    // Always use the full stored user (includes profile_picture and all fields)
    const storedUser = getStoredUser();
    const fullUser = storedUser || userData;
    setUser(fullUser);
    setIsLoggedIn(true);
    console.log('User authenticated:', fullUser);
    // Token is already stored in authService
  };

  // Handle logout
  const handleLogout = () => {
    logout(); // Clear localStorage
    setIsLoggedIn(false);
    setUser(null);
    console.log('User logged out');
  };

  // Open auth modal
  const handleOpenAuthModal = () => {
    setIsAuthModalOpen(true);
  };

  // Close auth modal
  const handleCloseAuthModal = () => {
    setIsAuthModalOpen(false);
  };

  return (
    <Router>
      <div className="min-h-screen bg-primary overflow-x-hidden">
        {/* Navigation */}
        <Navbar
          isLoggedIn={isLoggedIn}
          onOpenAuthModal={handleOpenAuthModal}
          onLogout={handleLogout}
          userName={user?.name}
        />

        {/* Auth Modal */}
        <AuthModal
          isOpen={isAuthModalOpen}
          onClose={handleCloseAuthModal}
          onAuthSuccess={handleAuthSuccess}
        />

        {/* Routes */}
        <Routes>
          {/* Home Page */}
          <Route
            path="/"
            element={
              <main>
                <Hero />
                <WhyUs />
                <HowItHelps />
              </main>
            }
          />

          {/* Protected Routes */}
          <Route
            path="/post-matrics"
            element={
              <ProtectedRoute onOpenAuthModal={handleOpenAuthModal}>
                <PostMatrics />
              </ProtectedRoute>
            }
          />
          <Route
            path="/analyze"
            element={
              <ProtectedRoute onOpenAuthModal={handleOpenAuthModal}>
                <Analyze />
              </ProtectedRoute>
            }
          />
          <Route
            path="/results"
            element={
              <ProtectedRoute onOpenAuthModal={handleOpenAuthModal}>
                <Results />
              </ProtectedRoute>
            }
          />
          <Route
            path="/create-resume"
            element={
              <ProtectedRoute onOpenAuthModal={handleOpenAuthModal}>
                <CreateResume />
              </ProtectedRoute>
            }
          />
          <Route
            path="/build-resume"
            element={
              <ProtectedRoute onOpenAuthModal={handleOpenAuthModal}>
                <BuildResume />
              </ProtectedRoute>
            }
          />
          <Route
            path="/routine-build"
            element={
              <ProtectedRoute onOpenAuthModal={handleOpenAuthModal}>
                <RoutineBuild />
              </ProtectedRoute>
            }
          />
          <Route
            path="/community"
            element={
              <ProtectedRoute onOpenAuthModal={handleOpenAuthModal}>
                <Community />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute onOpenAuthModal={handleOpenAuthModal}>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/explore"
            element={
              <ProtectedRoute onOpenAuthModal={handleOpenAuthModal}>
                <Explore />
              </ProtectedRoute>
            }
          />
          {/* Public reset password page — no auth required */}
          <Route path="/reset-password" element={<ResetPassword />} />
        </Routes>

        {/* Footer */}
        <Footer />
      </div>
    </Router>
  );
}

export default App;
