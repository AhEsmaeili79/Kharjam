"use client";

import { useEffect } from "react";
import { useLocaleStore } from "@/store/useLocaleStore";

const ChangeLocaleComponent = () => {
  const { locale, setLocale } = useLocaleStore();

  useEffect(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("locale");
      if (saved) setLocale(saved);
    }
  }, [setLocale]);

  const toggleLocale = () => {
    setLocale(locale === "fa" ? "en" : "fa");
  };

  return (
    <button
      onClick={toggleLocale}
      className="flex items-center justify-center size-12 rounded-full border-2 border-sky-400 text-sky-400 hover:bg-sky-100 dark:hover:bg-sky-900 transition"
    >
      {locale === "fa" ? "EN" : "FA"}
    </button>
  );
};

export default ChangeLocaleComponent;
