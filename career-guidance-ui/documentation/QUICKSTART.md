# 🚀 Quick Start Guide

## Installation & Setup

```bash
cd career-guidance-ui
npm install
npm start
```

The app will open at `http://localhost:3000`

## 🎮 Testing Features

### 1. Navigation
- Click on nav items to scroll to sections
- Try the mobile menu (resize browser)
- Click "Login" or "Sign Up" to toggle login state
- Notice "Profile" appears when logged in

### 2. Hero Section
- Watch the animated gradient shapes
- See floating particles
- Observe smooth entrance animations
- Check the scroll indicator at bottom

### 3. Why Us Section
- Hover over feature cards for glow effect
- Icons rotate on hover
- Scroll to trigger entrance animations

### 4. How It Helps Section
- See the 3-step timeline
- Hover over step cards
- Notice the connecting arrows (desktop)

### 5. Contact Section
- Fill out the contact form
- See focus glow effects on inputs
- Submit to test (logs to console)
- Check contact info cards

### 6. Footer
- Hover over social icons
- Test quick links
- Responsive layout

## 🎨 Customization

### Change Colors
Edit `tailwind.config.js` and `src/index.css`

### Modify Content
- **Hero text**: `src/components/Hero.jsx`
- **Features**: `src/components/WhyUs.jsx`
- **Steps**: `src/components/HowItHelps.jsx`
- **Contact info**: `src/components/Contact.jsx`

### Add New Sections
1. Create component in `src/components/`
2. Import in `src/App.js`
3. Add between existing sections

## 🔌 Backend Integration

### Authentication
Replace mock state in `App.js`:
```javascript
// Replace useState with actual API calls
const [isLoggedIn, setIsLoggedIn] = useState(false);
```

### Contact Form
Update `Contact.jsx` handleSubmit:
```javascript
const handleSubmit = async (e) => {
  e.preventDefault();
  const response = await fetch('/api/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  });
  // Handle response
};
```

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🎯 Key Features

✨ Glassmorphism design
✨ Smooth scroll animations
✨ Framer Motion effects
✨ Mobile responsive
✨ Login state management
✨ Contact form validation
✨ Hover glow effects
✨ Gradient backgrounds

## 🐛 Troubleshooting

### Animations not working?
- Check if Framer Motion is installed: `npm list framer-motion`
- Reinstall: `npm install framer-motion`

### Tailwind not applying?
- Restart dev server: `npm start`
- Check `tailwind.config.js` exists
- Verify `@tailwind` directives in `index.css`

### Icons not showing?
- Check Lucide React: `npm list lucide-react`
- Reinstall: `npm install lucide-react`

## 📚 Next Steps

1. Connect to backend API
2. Add authentication flow
3. Create dashboard pages
4. Implement career analysis
5. Add skill gap visualization
6. Build roadmap generator
7. Create peer matching system

Enjoy building! 🎉
