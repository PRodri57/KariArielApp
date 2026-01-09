module.exports = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#f7f2e9",
        dune: "#121413",
        ember: "#f08a4b",
        sea: "#4aa2ad",
        moss: "#8d9f7a",
        stone: "#2b2f2d",
        soot: "#0a0c0b",
        haze: "#181b1a"
      },
      fontFamily: {
        sans: ["Space Grotesk", "system-ui", "sans-serif"],
        display: ["Fraunces", "serif"]
      },
      boxShadow: {
        soft: "0 24px 60px -32px rgba(16, 19, 17, 0.45)",
        glow: "0 0 0 1px rgba(230, 127, 74, 0.35), 0 12px 30px -20px rgba(230, 127, 74, 0.8)"
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-6px)" }
        },
        rise: {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        },
        shimmer: {
          "0%": { backgroundPosition: "200% 0" },
          "100%": { backgroundPosition: "-200% 0" }
        }
      },
      animation: {
        float: "float 6s ease-in-out infinite",
        rise: "rise 0.6s ease-out both",
        shimmer: "shimmer 2.2s linear infinite"
      }
    }
  },
  plugins: []
};
