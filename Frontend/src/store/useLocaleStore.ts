import { create } from "zustand";

interface ILocaleState {
  locale: string;
  setLocale: (locale: string) => void;
}

export const useLocaleStore = create<ILocaleState>((set) => ({
  locale:
    typeof window !== "undefined" ? localStorage.getItem("lang") || "fa" : "fa",
  setLocale: (locale: string) => {
    set({ locale });
    if (typeof window !== "undefined") {
      localStorage.setItem("lang", locale);
    }
  },
}));
