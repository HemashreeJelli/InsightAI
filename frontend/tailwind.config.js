/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: {
          light: '#fdfbf7',   // Creamy extra-light paper
          DEFAULT: '#f9f6ef', // Warm classic editorial paper
          dark: '#f1ebd9',    // Slightly darker textured paper
        },
        accent: {
          orange: {
            light: '#ffedd5', // Very light orange tint
            DEFAULT: '#f97316', // Vibrant orange
            dark: '#ea580c',   // Deep amber orange
          }
        },
        charcoal: '#1c1c1c',  // Soft charcoal (easier on eyes than pure black)
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        body: ['"Lora"', 'Georgia', 'serif'],
        sans: ['"Outfit"', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'paper-sm': '0 2px 8px -2px rgba(28, 28, 28, 0.05)',
        'paper-md': '0 8px 24px -4px rgba(28, 28, 28, 0.08)',
        'orange-glow': '0 0 20px -2px rgba(249, 115, 22, 0.15)',
        'orange-glow-lg': '0 0 30px 2px rgba(249, 115, 22, 0.25)',
      },
      scale: {
        '102': '1.02',
      }
    },
  },
  plugins: [],
}
