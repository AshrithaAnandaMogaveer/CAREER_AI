import { Sun, Moon } from 'lucide-react';
import { motion } from 'framer-motion';

const ResumeToolbar = ({ previewTheme, onThemeToggle }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex items-center justify-between mb-4"
    >
      <h2 className="text-2xl font-bold text-white">Live Preview</h2>
      
      <div className="flex items-center space-x-2">
        <span className="text-sm text-gray-400">Preview Theme:</span>
        <button
          onClick={onThemeToggle}
          className="flex items-center space-x-2 px-3 py-2 glass rounded-lg hover:glow-cyan transition-all duration-300"
        >
          {previewTheme === 'light' ? (
            <>
              <Sun className="w-4 h-4 text-yellow-400" />
              <span className="text-sm text-white">Light</span>
            </>
          ) : (
            <>
              <Moon className="w-4 h-4 text-blue-400" />
              <span className="text-sm text-white">Dark</span>
            </>
          )}
        </button>
      </div>
    </motion.div>
  );
};

export default ResumeToolbar;
