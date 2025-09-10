import faMessages from "../messages/fa.json";
import enMessages from "../messages/en.json";

// Map of all supported locales to their message JSON
export const messagesMap: Record<string, any> = {
  fa: faMessages,
  en: enMessages,
};

// Optional: define supported locales and default
export const supportedLocales = ["fa", "en"] as const;
export const defaultLocale = "fa";
export type Locale = (typeof supportedLocales)[number];
