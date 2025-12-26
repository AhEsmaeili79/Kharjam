"use client";

import { useEffect, useState } from "react";
import { useLocaleStore } from "@/store/useLocaleStore";

const ChangeLocaleComponent = () => {
  const { locale, setLocale } = useLocaleStore();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("locale");
      if (saved && saved !== locale) {
        setLocale(saved);
      }
    }
  }, [setLocale, locale]);

  const toggleLocale = () => {
    setLocale(locale === "fa" ? "en" : "fa");
  };
  const currentLocale = mounted ? locale : "fa";

  return (
    <button
      onClick={toggleLocale}
      className="flex items-center justify-center size-12 rounded-full border-2 border-sky-400 text-sky-400 hover:bg-sky-100 dark:hover:bg-sky-900 transition"
    >
      {currentLocale === "fa" ? "EN" : "FA"}
    </button>
  );
};

export default ChangeLocaleComponent;
