"use client";

import { Toaster as Sonner } from "sonner";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { CheckCircle2, AlertTriangle, XCircle } from "lucide-react";
import { useLocaleStore } from "@/store/useLocaleStore";
import { defaultLocale } from "@/i18n";

type ToasterProps = React.ComponentProps<typeof Sonner>;

type Lang = "fa" | "en";

const baseOptions = {
  duration: 3000,
};

const isRTL = (lang: Lang) => lang === "fa";

const getLocale = (): Lang => {
  if (typeof window === "undefined") return defaultLocale as Lang;
  const locale = useLocaleStore.getState().locale;
  return (locale === "fa" || locale === "en" ? locale : defaultLocale) as Lang;
};

export function Toaster({ className, ...props }: ToasterProps) {
  return (
    <Sonner
      className={cn("toaster group", className)}
      toastOptions={{
        classNames: {
          toast:
            "group toast bg-background text-foreground border shadow-lg rounded-xl px-5 py-3 flex items-center justify-center gap-3 text-sm font-medium",
          description: "text-muted-foreground text-xs",
          actionButton:
            "inline-flex h-8 items-center justify-center rounded-md bg-primary text-primary-foreground text-xs font-medium px-3 shadow transition-all hover:bg-primary/90",
          cancelButton:
            "inline-flex h-8 items-center justify-center rounded-md border text-xs font-medium px-3 shadow-sm hover:bg-accent",
        },
      }}
      {...props}
    />
  );
}

export const notify = {
  success: (message: string, lang?: Lang) => {
    const currentLang = lang ?? getLocale();
    return toast(message, {
      ...baseOptions,
      icon: (
        <CheckCircle2
          className={`w-5 h-5 ${
            isRTL(currentLang)
              ? "order-2 text-green-500"
              : "order-1 text-green-500"
          }`}
        />
      ),
      classNames: {
        toast: `
          flex items-center gap-3 
          ${isRTL(currentLang) ? "flex-row-reverse text-right" : "text-left"}
          bg-green-50 border border-green-300 text-green-800
          dark:bg-green-900/30 dark:text-green-100 dark:border-green-700
          rounded-xl px-5 py-3 shadow-md`,
      },
    });
  },

  error: (message: string, lang?: Lang) => {
    const currentLang = lang ?? getLocale();
    return toast(message, {
      ...baseOptions,
      icon: (
        <XCircle
          className={`w-5 h-5 ${
            isRTL(currentLang)
              ? "order-2 text-red-500"
              : "order-1 text-red-500"
          }`}
        />
      ),
      classNames: {
        toast: `
          flex items-center gap-3 
          ${isRTL(currentLang) ? "flex-row-reverse text-right" : "text-left"}
          bg-red-50 border border-red-300 text-red-800
          dark:bg-red-900/30 dark:text-red-100 dark:border-red-700
          rounded-xl px-5 py-3 shadow-md`,
      },
    });
  },

  warning: (message: string, lang?: Lang) => {
    const currentLang = lang ?? getLocale();
    return toast(message, {
      ...baseOptions,
      icon: (
        <AlertTriangle
          className={`w-5 h-5 ${
            isRTL(currentLang)
              ? "order-2 text-yellow-500"
              : "order-1 text-yellow-500"
          }`}
        />
      ),
      classNames: {
        toast: `
          flex items-center gap-3 
          ${isRTL(currentLang) ? "flex-row-reverse text-right" : "text-left"}
          bg-yellow-50 border border-yellow-300 text-yellow-800
          dark:bg-yellow-900/30 dark:text-yellow-100 dark:border-yellow-700
          rounded-xl px-5 py-3 shadow-md`,
      },
    });
  },
};
