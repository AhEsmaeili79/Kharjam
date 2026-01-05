// src/store/useThemeStore.ts
import { create } from "zustand";

interface IThemeState {
  dark: boolean;
  toggleTheme: () => void;
}

const getInitialTheme = (): boolean => {
  // Always default to dark theme to prevent hydration mismatch
  // The actual theme will be applied via useEffect in the component
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
