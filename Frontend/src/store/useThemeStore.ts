// src/store/useThemeStore.ts
import { create } from "zustand";

interface IThemeState {
  dark: boolean;
  toggleTheme: () => void;
}

export const useThemeStore = create<IThemeState>((set, get) => ({
  dark: false,
  toggleTheme: () => {
    const current = get().dark;
    const newValue = !current;

    if (typeof document !== "undefined") {
      if (newValue) {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
    }

    set({ dark: newValue });
  },
}));
