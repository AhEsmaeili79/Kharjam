import { create } from "zustand";

type LocaleStore = {
  locale: string;
  setLocale: (locale: string) => void;
};

export const useLocaleStore = create<LocaleStore>((set) => ({
  locale: "fa", 
  setLocale: (locale) => {
    set({ locale });
    if (typeof window !== "undefined") {
      localStorage.setItem("locale", locale);
    }
  },
}));
