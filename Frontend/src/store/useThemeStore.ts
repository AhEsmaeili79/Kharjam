// src/store/useThemeStore.ts
import { create } from "zustand";

interface IThemeState {
  dark: boolean;
  toggleTheme: () => void;
}

const getInitialTheme = (): boolean => {
  if (typeof window !== "undefined") {
    const saved = localStorage.getItem("theme");
    if (saved) {
      return saved === "dark";
    }
    // If no theme saved, default to dark
    localStorage.setItem("theme", "dark");
    return true;
  }
  // Server-side default to dark
  return true;
};

export const useThemeStore = create<IThemeState>((set, get) => ({
  dark: getInitialTheme(),
  toggleTheme: () => {
    const current = get().dark;
    const newValue = !current;

    if (typeof document !== "undefined") {
      if (newValue) {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
      // Save to localStorage
      localStorage.setItem("theme", newValue ? "dark" : "light");
    }

    set({ dark: newValue });
  },
}));
