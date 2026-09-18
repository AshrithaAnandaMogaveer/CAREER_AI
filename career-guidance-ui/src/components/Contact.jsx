import { useState } from 'react';
import { motion } from 'framer-motion';
import { Mail, Linkedin, Github, Phone, MapPin, Send } from 'lucide-react';
import SectionWrapper from './SectionWrapper';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Backend integration point - send form data to API
    console.log('Form submitted:', formData);
    alert('Message sent! We will get back to you soon.');
    setFormData({ name: '', email: '', message: '' });
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const contactInfo = [
    { icon: Mail, label: 'Email', value: 'contact@careerai.com', href: 'mailto:contact@careerai.com' },
    { icon: Phone, label: 'Phone', value: '+1 (555) 123-4567', href: 'tel:+15551234567' },
    { icon: MapPin, label: 'Location', value: 'San Francisco, CA', href: '#' },
    { icon: Linkedin, label: 'LinkedIn', value: 'linkedin.com/company/careerai', href: 'https://linkedin.com' },
    { icon: Github, label: 'GitHub', value: 'github.com/careerai', href: 'https://github.com' },
  ];

  return (
    <SectionWrapper id="contact" className="py-16">
      <div className="max-w-6xl mx-auto">
        {/* Section Title */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-semibold mb-4 text-white">
            Get In Touch
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Have questions? We'd love to hear from you. Send us a message and we'll respond as soon as possible.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="bg-[#161625] rounded-xl p-8 border border-gray-700"
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Name Input */}
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-white mb-2">
                  Your Name
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 bg-[#0f0f1a] border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:border-[#00cccc] transition-all duration-200"
                  placeholder="John Doe"
                />
              </div>

              {/* Email Input */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-white mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 bg-[#0f0f1a] border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:border-[#00cccc] transition-all duration-200"
                  placeholder="john@example.com"
                />
              </div>

              {/* Message Input */}
              <div>
                <label htmlFor="message" className="block text-sm font-medium text-white mb-2">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows="5"
                  className="w-full px-4 py-3 bg-[#0f0f1a] border border-gray-700 rounded-md text-white placeholder-gray-500 focus:outline-none focus:border-[#00cccc] transition-all duration-200 resize-none"
                  placeholder="Tell us about your career goals..."
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                className="w-full px-6 py-3 bg-[#00cccc] text-black rounded-md font-semibold flex items-center justify-center space-x-2 hover:bg-[#00b3b3] transition-all duration-200"
              >
                <span>Send Message</span>
                <Send className="w-5 h-5" />
              </button>
            </form>
          </motion.div>

          {/* Contact Information */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="space-y-6"
          >
            <div className="bg-[#161625] rounded-xl p-8 border border-gray-700">
              <h3 className="text-xl font-semibold text-white mb-6">Contact Information</h3>
              <div className="space-y-4">
                {contactInfo.map((item, index) => {
                  const Icon = item.icon;
                  return (
                    <a
                      key={index}
                      href={item.href}
                      target={item.href.startsWith('http') ? '_blank' : '_self'}
                      rel="noopener noreferrer"
                      className="flex items-start space-x-4 p-4 rounded-lg hover:bg-[#0f0f1a] transition-all duration-200"
                    >
                      <div className="w-12 h-12 rounded-lg bg-[#00cccc]/10 border border-[#00cccc]/30 flex items-center justify-center flex-shrink-0">
                        <Icon className="w-6 h-6 text-[#00cccc]" />
                      </div>
                      <div>
                        <div className="text-sm text-gray-400">{item.label}</div>
                        <div className="text-white font-medium">{item.value}</div>
                      </div>
                    </a>
                  );
                })}
              </div>
            </div>

            {/* Additional Info Card */}
            <div className="bg-[#161625] rounded-xl p-8 border border-gray-700">
              <h4 className="text-lg font-semibold text-white mb-3">Office Hours</h4>
              <p className="text-gray-400 mb-2">Monday - Friday: 9:00 AM - 6:00 PM PST</p>
              <p className="text-gray-400">Saturday - Sunday: Closed</p>
              <div className="mt-4 pt-4 border-t border-gray-700">
                <p className="text-sm text-gray-400">
                  We typically respond within 24 hours during business days.
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </SectionWrapper>
  );
};

export default Contact;
