import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: { 
      colors: {
        text: {
          base: "var(--color-text-base)",
          secondary: "var(--color-text-secondary)",
          link: "var(--color-text-link)"
        },
        input: "var(--color-input)",
        back: "var(--color-back)"
      },
       },
  },
  plugins: [],
};

export default config;