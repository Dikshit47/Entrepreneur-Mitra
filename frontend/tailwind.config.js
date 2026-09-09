/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          primary: '#0F2C59',
          deep: '#0A1C38',
          tint: '#E8EEF5',
        },
        saffron: {
          primary: '#E85D04',
          hover: '#C44D00',
          tint: '#FFF3EB',
        },
        emerald: {
          primary: '#0B6E4F',
          tint: '#E6F4EA',
          dark: '#074D37',
        },
      },
    },
  },
  plugins: [],
}
