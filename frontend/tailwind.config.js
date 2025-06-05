export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./src/**/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        generale: ["Comfortaa", 'sans-serif'],
        secondary: ["Nunito", 'sans-serif'],  
      },
      fontSize: {
        'h1': ['56px', { lineHeight: '130%', fontWeight: '700' }],
        'h2': ['48px', { lineHeight: '100%', fontWeight: '700' }],
        'h3': ['40px', { lineHeight: '130%', fontWeight: '700' }],
        'h4': ['36px', { lineHeight: '130%', fontWeight: '700' }],
        'h5': ['32px', { lineHeight: '130%', fontWeight: '700' }],
        'h6': ['24px', { lineHeight: '130%', fontWeight: '700' }],
        'h7': ['16px', { lineHeight: '130%', fontWeight: '700' }],
        'body-1': ['24px', { lineHeight: '130%', fontWeight: '400' }],
        'body-2': ['20px', { lineHeight: '130%', fontWeight: '400' }],
        'body-3': ['16px', { lineHeight: '130%', fontWeight: '400' }],
        'body-4': ['14px', { lineHeight: '130%', fontWeight: '400' }],
        'body-5': ['12px', { lineHeight: '130%', fontWeight: '400' }],
        'body-6': ['10px', { lineHeight: '100%', fontWeight: '400' }],
        
      },
      colors: {
        black: {
          900: '#282828',
          800: '#3A3A3A',
          700: '#505050',
        },
        accent: {
          900: '#A0864D',
          600: '#B6975C',
          500: '#C2A06F'
        },
        primary: {
          300: '#BFBFBF'
        },
        background: {
          red: {
            200: '#FB3748',
            100: '#FF6636'
          },
          green: {
            100: '#2DB224',
          },
          blue: {
            100: '#2DA5F3'
          },
          primary: {
            500: '#949494'
          },
          accent: {
            700: '#A0864D'
          }
        }
      },
      
    },
    plugin: [],
  }
}
