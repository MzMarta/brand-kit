/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js,ts,jsx,tsx,md}"],
  theme: {
    extend: {
      colors: {
    "primary": {
        "hex": "#00529C"
    },
    "secondary": {
        "cyan": {
            "hex": "#00A3E0"
        },
        "darkGray": {
            "hex": "#333333"
        },
        "lightGray": {
            "hex": "#F4F4F4"
        }
    }
}
    }
  },
  plugins: [],
}
