"use client";

import { useEffect } from "react";
import { useThemeStore } from "@/store/useThemeStore";

const ThemeInitializer = () => {
  const { dark, _hasHydrated } = useThemeStore();

  useEffect(() => {
    if (_hasHydrated) {
      // Apply theme based on persisted store state
      if (dark) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    } else {
      // Fallback: check localStorage directly if store hasn't hydrated yet
      try {
        const theme = localStorage.getItem('theme');
        if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
      } catch (e) {
        // localStorage is not available
      }
    }
  }, [_hasHydrated, dark]);

  return null; // This component doesn't render anything
};

export default ThemeInitializer;
