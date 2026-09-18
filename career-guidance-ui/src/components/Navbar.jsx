import { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { Menu, X, User, Bell } from 'lucide-react';
import { Link } from 'react-router-dom';
import Button from './Button';
import { getStoredToken } from '../services/authService';

const Navbar = ({ isLoggedIn, onOpenAuthModal, onLogout, userName }) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Fetch notification count when user is logged in
  useEffect(() => {
    if (isLoggedIn) {
      fetchNotificationCount();
      // Poll for new notifications every 30 seconds
      const interval = setInterval(fetchNotificationCount, 30000);
      return () => clearInterval(interval);
    }
  }, [isLoggedIn]);

  const fetchNotificationCount = async () => {
    try {
      const token = getStoredToken();
      if (!token) return;

      const response = await fetch(
        'http://localhost:5000/api/community/notifications?unread_only=true',
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      if (data.success) {
        setUnreadCount(data.unread_count || 0);
      }
    } catch (error) {
      console.error('Error fetching notification count:', error);
    }
  };

  const navItems = [
    { name: 'Post Matrics', href: '/post-matrics', type: 'route' },
    { name: 'Analyze / Build', href: '/analyze', type: 'route' },
    { name: 'Routine Build', href: '/routine-build', type: 'route' },
    { name: 'Community', href: '/community', type: 'route' },
    { name: 'Explore', href: '/explore', type: 'route' },
  ];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-150 ${
        isScrolled ? 'bg-[#0f0f1a] border-b border-gray-800' : 'bg-[#0f0f1a]'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/">
            <div className="text-2xl font-semibold text-white cursor-pointer">
              CareerAI
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              item.type === 'route' ? (
                <Link
                  key={item.name}
                  to={item.href}
                  className="relative text-gray-400 hover:text-white transition-colors duration-150 font-medium group"
                >
                  {item.name}
                  <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#00cccc] group-hover:w-full transition-all duration-150"></span>
                </Link>
              ) : (
                <a
                  key={item.name}
                  href={item.href}
                  className="relative text-gray-400 hover:text-white transition-colors duration-150 font-medium group"
                >
                  {item.name}
                  <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#00cccc] group-hover:w-full transition-all duration-150"></span>
                </a>
              )
            ))}
          </div>

          {/* Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            <AnimatePresence mode="wait">
              {!isLoggedIn ? (
                <div className="flex items-center space-x-4">
                  <Button variant="primary" onClick={onOpenAuthModal}>
                    Login / Sign Up
                  </Button>
                </div>
              ) : (
                <div className="flex items-center space-x-4">
                  <Link
                    to="/profile"
                    className="relative flex items-center space-x-2 px-4 py-2 rounded-md bg-[#161625] border border-gray-700 text-gray-300 hover:border-[#00cccc] hover:text-white transition-colors"
                  >
                    <Bell size={18} />
                    {unreadCount > 0 && (
                      <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center animate-pulse">
                        {unreadCount > 99 ? '99+' : unreadCount}
                      </span>
                    )}
                  </Link>
                  <Link
                    to="/profile"
                    className="flex items-center space-x-2 px-4 py-2 rounded-md bg-[#161625] border border-gray-700 text-gray-300 hover:border-[#00cccc] hover:text-white transition-colors"
                  >
                    <User size={18} />
                    <span className="text-sm font-medium">{userName || 'Profile'}</span>
                  </Link>
                  <Button variant="secondary" onClick={onLogout}>
                    Logout
                  </Button>
                </div>
              )}
            </AnimatePresence>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-white"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X size={28} /> : <Menu size={28} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <div className="md:hidden bg-[#0f0f1a] border-t border-gray-800">
            <div className="px-6 py-4 space-y-4">
              {navItems.map((item) => (
                item.type === 'route' ? (
                  <Link
                    key={item.name}
                    to={item.href}
                    className="block text-gray-400 hover:text-white transition-colors font-medium"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {item.name}
                  </Link>
                ) : (
                  <a
                    key={item.name}
                    href={item.href}
                    className="block text-gray-400 hover:text-white transition-colors font-medium"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {item.name}
                  </a>
                )
              ))}
              <div className="pt-4 space-y-2">
                {!isLoggedIn ? (
                  <Button
                    variant="primary"
                    className="w-full"
                    onClick={() => {
                      onOpenAuthModal();
                      setIsMobileMenuOpen(false);
                    }}
                  >
                    Login / Sign Up
                  </Button>
                ) : (
                  <>
                    <Link
                      to="/profile"
                      className="relative block px-4 py-3 rounded-md bg-[#161625] border border-gray-700 text-center font-medium text-gray-300 hover:border-[#00cccc] hover:text-white transition-colors"
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      <Bell size={18} className="inline mr-2" />
                      Notifications
                      {unreadCount > 0 && (
                        <span className="ml-2 bg-red-500 text-white text-xs font-bold rounded-full px-2 py-1">
                          {unreadCount > 99 ? '99+' : unreadCount}
                        </span>
                      )}
                    </Link>
                    <Link
                      to="/profile"
                      className="block px-4 py-3 rounded-md bg-[#161625] border border-gray-700 text-center font-medium text-gray-300 hover:border-[#00cccc] hover:text-white transition-colors"
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      <User size={18} className="inline mr-2" />
                      {userName || 'Profile'}
                    </Link>
                    <Button
                      variant="secondary"
                      className="w-full"
                      onClick={() => {
                        onLogout();
                        setIsMobileMenuOpen(false);
                      }}
                    >
                      Logout
                    </Button>
                  </>
                )}
              </div>
            </div>
          </div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;
