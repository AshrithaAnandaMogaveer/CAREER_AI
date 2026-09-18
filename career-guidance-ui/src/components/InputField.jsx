import React from 'react';
import { motion } from 'framer-motion';

const InputField = ({ 
  label, 
  type = 'text', 
  name, 
  value, 
  onChange, 
  error, 
  placeholder,
  required = false 
}) => {
  return (
    <div className="w-full">
      <label htmlFor={name} className="block text-sm font-medium text-gray-300 mb-2">
        {label} {required && <span className="text-red-400">*</span>}
      </label>
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className={`w-full px-4 py-3 bg-white/5 border ${
          error ? 'border-red-500' : 'border-white/10'
        } rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 transition-all duration-300`}
      />
      {error && (
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-red-400 text-xs mt-1"
        >
          {error}
        </motion.p>
      )}
    </div>
  );
};

export default InputField;
