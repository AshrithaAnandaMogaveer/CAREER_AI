/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-lavender': '#8b80f9',
        'primary-blue': '#3b82f6',
        'bg-light-lavender': '#f5f3ff',
        'border-neutral': '#e5e7eb',
        'text-primary': '#1f2937',
        'text-secondary': '#6b7280',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
