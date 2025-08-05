import type { Config } from 'tailwindcss'

export default <Config>{
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#181924',
        accent: '#67F7D0'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heebo: ['Heebo', 'sans-serif']
      },
      boxShadow: {
        glow: '0 0 10px rgba(103, 247, 208, 0.5)'
      }
    }
  },
  plugins: []
}
