# CareerAI - Project Structure

## 🎨 Design System

### Color Palette
- **Background**: `#0f172a` (Dark Blue)
- **Accent Gradient**: Purple → Blue (`from-purple-600 to-blue-600`)
- **Card Background**: `rgba(255,255,255,0.05)` (Glassmorphism)
- **Glow Effects**: Soft Cyan / Violet
- **Text**: White / Soft Gray

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 800

## 📁 Component Structure

```
src/
├── components/
│   ├── Navbar.jsx          # Fixed navigation with login state
│   ├── Hero.jsx            # Landing hero section with animations
│   ├── WhyUs.jsx           # Feature cards section
│   ├── HowItHelps.jsx      # 3-step timeline flow
│   ├── Contact.jsx         # Contact form + info
│   ├── Footer.jsx          # Footer with links
│   ├── Button.jsx          # Reusable button component
│   ├── Card.jsx            # Reusable glassmorphism card
│   └── SectionWrapper.jsx  # Reusable section container
├── App.js                  # Main app component
├── index.js                # Entry point
└── index.css               # Global styles + Tailwind
```

## 🔌 Backend Integration Points

### 1. Authentication (Navbar.jsx)
```javascript
// Current: Mock state with useState
const [isLoggedIn, setIsLoggedIn] = useState(false);

// TODO: Replace with actual auth API
// - POST /api/auth/login
// - POST /api/auth/signup
// - POST /api/auth/logout
// - GET /api/auth/user (check session)
```

### 2. Contact Form (Contact.jsx)
```javascript
const handleSubmit = (e) => {
  e.preventDefault();
  // TODO: Send to backend
  // POST /api/contact
  // Body: { name, email, message }
};
```

### 3. User Profile (Future)
```javascript
// TODO: Add profile page
// GET /api/user/profile
// PUT /api/user/profile
```

### 4. Career Analysis (Future)
```javascript
// TODO: Add resume upload
// POST /api/analyze/resume
// POST /api/analyze/skills
// GET /api/career/roadmap
```

## 🚀 Running the Project

### Development
```bash
cd career-guidance-ui
npm install
npm start
```

### Build for Production
```bash
npm run build
```

## 📦 Dependencies

- **react**: ^19.2.4
- **react-dom**: ^19.2.4
- **framer-motion**: For animations
- **lucide-react**: For icons
- **tailwindcss**: ^4.1.18
- **autoprefixer**: ^10.4.24
- **postcss**: ^8.5.6

## 🎯 Features Implemented

✅ Responsive navbar with mobile menu
✅ Login/logout state management
✅ Animated hero section with floating particles
✅ 8 feature cards with hover effects
✅ 3-step timeline visualization
✅ Contact form with validation
✅ Professional footer
✅ Glassmorphism design throughout
✅ Smooth scroll animations
✅ Gradient backgrounds
✅ Glow effects on hover

## 🔮 Future Enhancements

- [ ] Connect to backend API
- [ ] Add dashboard after login
- [ ] Implement resume upload
- [ ] Add skill gap analysis page
- [ ] Create roadmap visualization
- [ ] Add peer matching feature
- [ ] Implement progress tracking
- [ ] Add course recommendations

## 🎨 Design Philosophy

This UI follows a **premium AI SaaS aesthetic**:
- Dreamy futuristic theme
- Soft gradients (purple, blue, cyan)
- Glassmorphism cards
- Smooth animations
- Professional typography
- Clean, modern layout
- Fully responsive
- Component-based architecture

## 📝 Notes

- All components are modular and reusable
- Login state is mock (ready for backend)
- Form submissions log to console (ready for API)
- All animations use Framer Motion
- Tailwind CSS for styling
- Mobile-first responsive design
