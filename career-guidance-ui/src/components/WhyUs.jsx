import { motion } from 'framer-motion';
import {
  Brain,
  Target,
  TrendingUp,
  Map,
  BookOpen,
  Users,
  Sparkles,
  BarChart3,
} from 'lucide-react';
import Card from './Card';
import SectionWrapper from './SectionWrapper';

const WhyUs = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Skill Extraction',
      description: 'Advanced NLP algorithms extract and analyze your skills from resumes and profiles with precision.',
    },
    {
      icon: Target,
      title: 'Career Feasibility Scoring',
      description: 'Get data-driven scores on career paths based on your current skill set and market demand.',
    },
    {
      icon: TrendingUp,
      title: 'Skill Gap Intelligence Engine',
      description: 'Identify exactly what skills you need to acquire to reach your dream career.',
    },
    {
      icon: Map,
      title: 'Graph-Based Roadmap Generator',
      description: 'Visual, structured learning paths tailored to your goals and current expertise.',
    },
    {
      icon: BookOpen,
      title: 'Content-Based Course Recommendation',
      description: 'Personalized course suggestions from top platforms matched to your learning needs.',
    },
    {
      icon: Users,
      title: 'AI-Driven Peer Matching',
      description: 'Connect with like-minded professionals and mentors on similar career journeys.',
    },
    {
      icon: Sparkles,
      title: 'Generative AI Personalized Guidance',
      description: 'Real-time AI coaching and career advice tailored specifically to your situation.',
    },
    {
      icon: BarChart3,
      title: 'Progress Tracking Analytics',
      description: 'Monitor your skill development and career readiness with comprehensive dashboards.',
    },
  ];

  return (
    <SectionWrapper id="why-us" className="py-16">
      <div className="max-w-7xl mx-auto">
        {/* Section Title */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-semibold mb-4 text-white">
            Why Choose Us?
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Cutting-edge AI technology meets career development expertise
          </p>
        </motion.div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card key={index} delay={index * 0.1}>
                <div className="flex flex-col items-center text-center space-y-4">
                  <div className="w-14 h-14 rounded-lg bg-[#00cccc]/10 border border-[#00cccc]/30 flex items-center justify-center">
                    <Icon className="w-7 h-7 text-[#00cccc]" />
                  </div>
                  <h3 className="text-lg font-semibold text-white">
                    {feature.title}
                  </h3>
                  <p className="text-gray-400 text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    </SectionWrapper>
  );
};

export default WhyUs;
