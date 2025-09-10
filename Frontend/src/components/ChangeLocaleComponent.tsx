"use client";

import { useLocaleStore } from "@/store/useLocaleStore";
const ChangeLocaleComponent = () => {
  const { locale, setLocale } = useLocaleStore();

  const languages = ["fa", "en"];

  return (
    <div className="flex gap-2">
      {languages.map((lang) => (
        <button
          key={lang}
          disabled={locale === lang}
          className={`px-2 py-1 border rounded ${
            locale === lang ? "bg-blue-500 text-white" : ""
          }`}
          onClick={() => setLocale(lang)}
        >
          {lang === "fa" ? "فارسی" : "English"}
        </button>
      ))}
    </div>
  );
};
export default ChangeLocaleComponent;
