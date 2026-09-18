import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Button from './Button';

const Hero = () => {
  const navigate = useNavigate();

  const handleExploreFeatures = () => {
    const section = document.getElementById('why-us');
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleGetStarted = () => {
    navigate('/post-matrics');
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center pt-16 bg-[#0f0f1a]">
      <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-6"
        >
          {/* Title */}
          <h1 className="text-5xl md:text-6xl font-semibold leading-tight text-white">
            Intelligent Career
            <br />
            <span className="text-[#00cccc]">Guidance System</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-400 font-normal">
            Powered by Skill Gap Intelligence & Generative AI
          </p>

          {/* Description */}
          <p className="text-gray-400 text-base max-w-2xl mx-auto leading-relaxed">
            Transform your career journey with AI-driven insights, personalized roadmaps,
            and intelligent skill gap analysis. Your future starts here.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
            <Button variant="primary" onClick={handleGetStarted}>Get Started</Button>
            <Button variant="secondary" onClick={handleExploreFeatures}>Explore Features</Button>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;
