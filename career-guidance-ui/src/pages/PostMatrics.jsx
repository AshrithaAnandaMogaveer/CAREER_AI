import { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  GraduationCap, 
  BookOpen, 
  Trophy, 
  Briefcase, 
  Award, 
  Brain,
  ArrowLeft
} from 'lucide-react';
import Button from '../components/Button';

// Import sub-components
import After10thGuidance from '../components/postMatrics/After10thGuidance';
import After12thGuidance from '../components/postMatrics/After12thGuidance';
import CompetitiveExams from '../components/postMatrics/CompetitiveExams';
import SkillBasedCareers from '../components/postMatrics/SkillBasedCareers';
import Scholarships from '../components/postMatrics/Scholarships';
import InterestTest from '../components/postMatrics/InterestTest';

const PostMatrics = () => {
  const [selectedTab, setSelectedTab] = useState(null);

  const tabs = [
    {
      id: 'after10th',
      icon: GraduationCap,
      title: 'After 10th Guidance',
      description: 'Explore stream options after 10th grade',
      gradient: 'from-purple-500 to-pink-500',
    },
    {
      id: 'after12th',
      icon: BookOpen,
      title: 'After 12th Guidance',
      description: 'Discover career paths after 12th',
      gradient: 'from-blue-500 to-cyan-500',
    },
    {
      id: 'exams',
      icon: Trophy,
      title: 'Competitive Exams',
      description: 'Find the right exams for you',
      gradient: 'from-orange-500 to-red-500',
    },
    {
      id: 'skills',
      icon: Briefcase,
      title: 'Skill-Based Careers',
      description: 'Explore skill-based opportunities',
      gradient: 'from-green-500 to-emerald-500',
    },
    {
      id: 'scholarships',
      icon: Award,
      title: 'Scholarships',
      description: 'Find financial aid options',
      gradient: 'from-yellow-500 to-orange-500',
    },
    {
      id: 'interest',
      icon: Brain,
      title: 'Interest Assessment',
      description: 'Take aptitude test',
      gradient: 'from-indigo-500 to-purple-500',
    },
  ];

  const renderContent = () => {
    switch (selectedTab) {
      case 'after10th':
        return <After10thGuidance />;
      case 'after12th':
        return <After12thGuidance />;
      case 'exams':
        return <CompetitiveExams />;
      case 'skills':
        return <SkillBasedCareers />;
      case 'scholarships':
        return <Scholarships />;
      case 'interest':
        return <InterestTest />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-primary pt-32 pb-20 px-6">
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 90, 0],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
          className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            scale: [1.2, 1, 1.2],
            rotate: [90, 0, 90],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{ duration: 15, repeat: Infinity, ease: 'linear' }}
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl"
        />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              Post Matrics
            </span>
            <br />
            <span className="text-white">Guidance</span>
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Navigate your educational journey with AI-powered career guidance
          </p>
        </motion.div>

        {!selectedTab ? (
          /* Category Grid */
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tabs.map((tab, index) => (
              <motion.div
                key={tab.id}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                whileHover={{ y: -10, scale: 1.02 }}
                onClick={() => setSelectedTab(tab.id)}
                className="glass rounded-2xl p-8 cursor-pointer hover:glow-violet transition-all duration-300"
              >
                <div className="flex flex-col items-center text-center space-y-4">
                  <motion.div
                    whileHover={{ rotate: 360, scale: 1.1 }}
                    transition={{ duration: 0.6 }}
                    className={`w-16 h-16 rounded-full bg-gradient-to-br ${tab.gradient} bg-opacity-20 flex items-center justify-center glow-violet`}
                  >
                    <tab.icon className="w-8 h-8 text-white" />
                  </motion.div>
                  <h3 className="text-xl font-semibold text-white">{tab.title}</h3>
                  <p className="text-gray-400 text-sm">{tab.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          /* Selected Tab Content */
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="mb-6">
              <Button
                variant="secondary"
                onClick={() => setSelectedTab(null)}
                className="flex items-center space-x-2"
              >
                <ArrowLeft size={18} />
                <span>Back to Categories</span>
              </Button>
            </div>

            <div className="glass rounded-2xl p-8 glow-violet">
              {renderContent()}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default PostMatrics;
