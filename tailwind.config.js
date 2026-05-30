/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nav: '#101828',
        background: '#f7ede2',
        card: '#ffffff',
        accent: '#fbbf24', // yellow
        orange: {
          light: '#fef3c7',
          DEFAULT: '#f59e0b',
        },
        blue: {
          light: '#dbeafe',
          DEFAULT: '#3b82f6',
        },
        yellow: {
          light: '#fef08a',
          DEFAULT: '#fbbf24',
        },
        green: {
          DEFAULT: '#10b981',
        },
        red: {
          DEFAULT: '#ef4444',
        }
      }
    },
  },
  plugins: [],
}
