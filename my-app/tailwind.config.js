module.exports = {
  darkMode: "class",
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: { sans: ["var(--font-inter)", "sans-serif"] },
      colors: { primary: "#3B82F6" },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
