import { useEffect, useState } from "react";
import { useLocaleStore } from "@/store/useLocaleStore"; // adjust path to your stores
import { messagesMap, defaultLocale } from "@/i18n";

export const useLocale = () => {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  const locale = useLocaleStore((state) => state.locale);
  const currentLocale = mounted ? locale : defaultLocale;
  const messages = messagesMap[currentLocale];

  useEffect(() => {
    if (typeof document !== "undefined") {
      document.documentElement.lang = locale;
      document.documentElement.dir = locale === "fa" ? "rtl" : "ltr";
    }
  }, [locale]);

  return { mounted, locale, currentLocale, messages };
};
