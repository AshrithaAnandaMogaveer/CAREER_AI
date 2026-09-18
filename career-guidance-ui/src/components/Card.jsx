import { motion } from 'framer-motion';

const Card = ({ children, className = '', delay = 0 }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay }}
      className={`bg-[#161625] border border-gray-700 rounded-xl p-6 hover:border-[#00cccc] transition-all duration-150 ${className}`}
    >
      {children}
    </motion.div>
  );
};

export default Card;
