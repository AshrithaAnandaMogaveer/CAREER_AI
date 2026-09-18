# 🚀 Deployment Guide

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## Deployment Options

### 1. Vercel (Recommended for React)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Or connect your GitHub repo to Vercel dashboard for automatic deployments.

### 2. Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

Or drag and drop the `build/` folder to Netlify dashboard.

### 3. GitHub Pages

Add to `package.json`:
```json
"homepage": "https://yourusername.github.io/career-guidance-ui"
```

Install gh-pages:
```bash
npm install --save-dev gh-pages
```

Add scripts:
```json
"predeploy": "npm run build",
"deploy": "gh-pages -d build"
```

Deploy:
```bash
npm run deploy
```

### 4. AWS S3 + CloudFront

```bash
# Build
npm run build

# Upload to S3
aws s3 sync build/ s3://your-bucket-name

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

### 5. Docker

Create `Dockerfile`:
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build and run:
```bash
docker build -t career-guidance-ui .
docker run -p 80:80 career-guidance-ui
```

## Environment Variables

Create `.env` file for different environments:

```env
# .env.development
REACT_APP_API_URL=http://localhost:5000/api

# .env.production
REACT_APP_API_URL=https://api.yourdomain.com/api
```

Access in code:
```javascript
const API_URL = process.env.REACT_APP_API_URL;
```

## Performance Optimization

### 1. Code Splitting
Already implemented with React lazy loading (if needed):
```javascript
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
```

### 2. Image Optimization
- Use WebP format
- Compress images
- Lazy load images

### 3. Bundle Analysis
```bash
npm install --save-dev webpack-bundle-analyzer
npm run build
npx webpack-bundle-analyzer build/static/js/*.js
```

### 4. Lighthouse Score
Run in Chrome DevTools:
- Performance: 90+
- Accessibility: 95+
- Best Practices: 95+
- SEO: 90+

## Backend Integration

### API Configuration

Create `src/config/api.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const API_ENDPOINTS = {
  auth: {
    login: `${API_BASE_URL}/auth/login`,
    signup: `${API_BASE_URL}/auth/signup`,
    logout: `${API_BASE_URL}/auth/logout`,
  },
  contact: `${API_BASE_URL}/contact`,
  career: {
    analyze: `${API_BASE_URL}/career/analyze`,
    roadmap: `${API_BASE_URL}/career/roadmap`,
  },
};
```

### CORS Configuration

Backend needs to allow frontend origin:
```javascript
// Express.js example
app.use(cors({
  origin: 'https://yourdomain.com',
  credentials: true
}));
```

## SSL/HTTPS

Most hosting providers (Vercel, Netlify) provide free SSL.

For custom domains:
- Use Let's Encrypt
- Configure in your hosting provider
- Update API URLs to use HTTPS

## Monitoring & Analytics

### Google Analytics
Add to `public/index.html`:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Error Tracking
Use Sentry:
```bash
npm install @sentry/react
```

```javascript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  environment: process.env.NODE_ENV,
});
```

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Build
        run: npm run build
      - name: Deploy
        run: npm run deploy
```

## Security Checklist

- [ ] Enable HTTPS
- [ ] Set security headers
- [ ] Implement CSP (Content Security Policy)
- [ ] Sanitize user inputs
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting on API
- [ ] Implement authentication properly
- [ ] Regular dependency updates

## Post-Deployment

1. Test all features in production
2. Check mobile responsiveness
3. Verify API connections
4. Test form submissions
5. Check analytics tracking
6. Monitor error logs
7. Set up uptime monitoring

## Rollback Strategy

Keep previous builds:
```bash
# Tag releases
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Rollback if needed
git checkout v1.0.0
npm run deploy
```

## Support

For issues:
1. Check browser console
2. Verify API endpoints
3. Check network tab
4. Review error logs
5. Test in incognito mode

Happy deploying! 🎉
