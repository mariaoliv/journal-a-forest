/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        earth: {
          50: '#faf9f7',
          100: '#f5f3ef',
          200: '#e8e4db',
          300: '#d4ccc0',
          400: '#b8ab9b',
          500: '#9f8f7e',
          600: '#877a6b',
          700: '#6f6458',
          800: '#5c5249',
          900: '#4d453d',
        },
        forest: {
          50: '#f0f7f4',
          100: '#dcf0e8',
          200: '#bce1d2',
          300: '#90cbb3',
          400: '#5dab8e',
          500: '#3d8f70',
          600: '#2d735a',
          700: '#265d4a',
          800: '#224b3d',
          900: '#1e3f34',
        },
        cream: {
          50: '#fefdfb',
          100: '#fdf9f2',
          200: '#faf2e0',
          300: '#f6e8c8',
          400: '#f0d9a8',
          500: '#e8c884',
          600: '#deb15f',
          700: '#c89444',
          800: '#a67838',
          900: '#866332',
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '50%': { transform: 'translateY(-10px) rotate(5deg)' },
        },
      },
    },
  },
  plugins: [],
}

