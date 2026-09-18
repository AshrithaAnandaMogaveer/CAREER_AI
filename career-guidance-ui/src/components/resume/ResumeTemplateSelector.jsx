import { motion } from 'framer-motion';
import { FileText, Layout, Columns, Briefcase, Code } from 'lucide-react';

const templates = [
  {
    id: 'modern',
    name: 'Modern Professional',
    icon: FileText,
    description: 'Clean and modern design',
  },
  {
    id: 'minimal',
    name: 'Minimal Clean',
    icon: Layout,
    description: 'Simple and elegant',
  },
  {
    id: 'executive',
    name: 'Two-Column Executive',
    icon: Columns,
    description: 'Professional two-column layout',
  },
  {
    id: 'fresher',
    name: 'Fresher Compact',
    icon: Briefcase,
    description: 'Perfect for entry-level',
  },
  {
    id: 'technical',
    name: 'Technical Profile',
    icon: Code,
    description: 'Ideal for tech roles',
  },
];

const ResumeTemplateSelector = ({ selectedTemplate, onSelectTemplate }) => {
  return (
    <div>
      <h2 className="text-xl font-semibold text-white mb-4">Choose Template</h2>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {templates.map((template) => (
          <motion.button
            key={template.id}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onSelectTemplate(template.id)}
            className={`glass rounded-lg p-4 transition-all duration-300 ${
              selectedTemplate === template.id
                ? 'bg-gradient-to-r from-cyan-600/30 to-blue-600/30 glow-cyan border-2 border-cyan-500'
                : 'hover:glow-violet'
            }`}
          >
            <template.icon className="w-8 h-8 text-cyan-400 mx-auto mb-2" />
            <p className="text-white text-sm font-medium mb-1">{template.name}</p>
            <p className="text-gray-400 text-xs">{template.description}</p>
          </motion.button>
        ))}
      </div>
    </div>
  );
};

export default ResumeTemplateSelector;
