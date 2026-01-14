module.exports = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "rgb(var(--ink) / <alpha-value>)",
        dune: "rgb(var(--dune) / <alpha-value>)",
        ember: "rgb(var(--ember) / <alpha-value>)",
        sea: "rgb(var(--sea) / <alpha-value>)",
        moss: "rgb(var(--moss) / <alpha-value>)",
        stone: "rgb(var(--stone) / <alpha-value>)",
        soot: "rgb(var(--soot) / <alpha-value>)",
        haze: "rgb(var(--haze) / <alpha-value>)"
      },
      fontFamily: {
        sans: ["Space Grotesk", "system-ui", "sans-serif"],
        display: ["Fraunces", "serif"]
      },
      boxShadow: {
        soft: "var(--shadow-soft)",
        glow: "var(--shadow-glow)"
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
