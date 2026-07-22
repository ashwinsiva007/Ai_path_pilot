/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0B0F19',
        surface: '#1A2332',
        primary: '#3B82F6',
        secondary: '#10B981',
        textPrimary: '#F3F4F6',
        textSecondary: '#9CA3AF'
      }
    },
  },
  plugins: [],
}
