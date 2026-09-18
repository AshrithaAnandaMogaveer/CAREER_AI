import { motion } from 'framer-motion';

const Footer = () => {
  const quickLinks = [
    { name: 'About Us', href: '#about' },
    { name: 'Features', href: '#why-us' },
    { name: 'How It Works', href: '#how-it-helps' },
    { name: 'Contact', href: '#contact' },
  ];

  const resources = [
    { name: 'Documentation', href: '/docs' },
    { name: 'API Reference', href: '/api' },
    { name: 'Blog', href: '/blog' },
    { name: 'Support', href: '/support' },
  ];

  const socialLinks = [];

  return (
    <footer className="relative bg-[#0a0a12] border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-6 md:px-12 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Section */}
          <div className="col-span-1 md:col-span-2">
            <div className="text-2xl font-semibold text-white mb-4">
              CareerAI
            </div>
            <p className="text-gray-400 text-sm leading-relaxed max-w-md mb-6">
              Empowering careers through intelligent AI-driven guidance, skill gap analysis, 
              and personalized learning pathways. Your future starts here.
            </p>
            {/* Social Links */}
            <div className="flex space-x-4">
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              {quickLinks.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-gray-400 hover:text-[#00cccc] text-sm transition-colors duration-200"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-white font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              {resources.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-gray-400 hover:text-[#00cccc] text-sm transition-colors duration-200"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              © {new Date().getFullYear()} CareerAI. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
