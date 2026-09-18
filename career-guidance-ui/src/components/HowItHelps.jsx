import { motion } from 'framer-motion';
import { Upload, LineChart, Rocket } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import SectionWrapper from './SectionWrapper';

const HowItHelps = () => {
  const navigate = useNavigate();

  const steps = [
    {
      icon: Upload,
      title: 'Upload Resume / Enter Skills',
      description: 'Share your resume or manually input your skills. Our AI instantly analyzes your profile.',
    },
    {
      icon: LineChart,
      title: 'Get Career Readiness Score & Gap Analysis',
      description: 'Receive detailed insights on your career readiness and identify skill gaps holding you back.',
    },
    {
      icon: Rocket,
      title: 'Follow Structured Roadmap & Connect',
      description: 'Access personalized learning paths, connect with peers, and track your progress in real-time.',
    },
  ];

  return (
    <SectionWrapper id="how-it-helps" className="py-16">
      <div className="max-w-6xl mx-auto">
        {/* Section Title */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <h2 className="text-3xl font-semibold mb-4 text-white">
            How It Helps You
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Three simple steps to transform your career trajectory
          </p>
        </motion.div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="relative"
              >
                {/* Step Card */}
                <div className="bg-[#161625] rounded-xl p-8 border border-gray-700 hover:border-[#00cccc] transition-all duration-200 relative">
                  {/* Step Number */}
                  <div className="absolute -top-4 -left-4 w-12 h-12 rounded-full bg-[#00cccc] flex items-center justify-center text-black font-bold text-xl">
                    {index + 1}
                  </div>

                  {/* Icon */}
                  <div className="w-16 h-16 rounded-lg bg-[#00cccc]/10 border border-[#00cccc]/30 flex items-center justify-center mb-6 mx-auto">
                    <Icon className="w-8 h-8 text-[#00cccc]" />
                  </div>

                  {/* Content */}
                  <h3 className="text-lg font-semibold text-white mb-3 text-center">
                    {step.title}
                  </h3>
                  <p className="text-gray-400 text-sm leading-relaxed text-center">
                    {step.description}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="text-center mt-16"
        >
          <p className="text-gray-400 mb-6 text-lg">Ready to accelerate your career?</p>
          <button 
            onClick={() => navigate('/post-matrics')}
            className="px-10 py-3 bg-[#00cccc] text-black rounded-md font-semibold hover:bg-[#00b3b3] transition-all duration-200"
          >
            Start Your Journey
          </button>
        </motion.div>
      </div>
    </SectionWrapper>
  );
};

export default HowItHelps;
