import React from 'react';
import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../services/authService';

/**
 * Protected Route Component
 * Redirects to home if user is not authenticated
 */
const ProtectedRoute = ({ children, onOpenAuthModal }) => {
  const authenticated = isAuthenticated();

  if (!authenticated) {
    // Open auth modal and redirect to home
    if (onOpenAuthModal) {
      setTimeout(() => onOpenAuthModal(), 100);
    }
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;
