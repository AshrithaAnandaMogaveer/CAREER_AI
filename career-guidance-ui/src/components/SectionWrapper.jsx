import React from 'react';
import { motion } from 'framer-motion';

const SectionWrapper = ({ children, className = '', id = '' }) => {
  return (
    <motion.section
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.8 }}
      id={id}
      className={`py-20 px-6 md:px-12 lg:px-24 relative ${className}`}
    >
      {children}
    </motion.section>
  );
};

export default SectionWrapper;
