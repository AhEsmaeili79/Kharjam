import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

interface IThemeState {
  dark: boolean;
  toggleTheme: () => void;
  setTheme: (dark: boolean) => void;
  _hasHydrated: boolean;
  setHasHydrated: (hasHydrated: boolean) => void;
}

export const useThemeStore = create<IThemeState>()(
  persist(
    (set, get) => ({
      dark: false,
      _hasHydrated: false,
      setHasHydrated: (hasHydrated: boolean) => set({ _hasHydrated: hasHydrated }),
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
      setTheme: (dark: boolean) => {
        if (typeof document !== "undefined") {
          if (dark) {
            document.documentElement.classList.add("dark");
          } else {
            document.documentElement.classList.remove("dark");
          }
        }

        set({ dark });
      },
    }),
    {
      name: "theme-storage",
      storage: createJSONStorage(() => localStorage),
      onRehydrateStorage: () => (state) => {
        if (state) {
          state.setHasHydrated(true);
        }
      },
    }
  )
);
