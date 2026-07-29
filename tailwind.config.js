/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./frontend/**/*.html",
    "./frontend/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#10b981', /* Emerald 500 */
        primaryHover: '#059669', /* Emerald 600 */
        dark: '#070a13',
        slateDark: '#0b0f19',
      },
      fontFamily: {
        sans: ['Outfit', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
