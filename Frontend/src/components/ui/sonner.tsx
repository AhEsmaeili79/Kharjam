"use client";

import { Toaster as Sonner } from "sonner";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { useLocaleStore } from "@/store/useLocaleStore";
import { defaultLocale } from "@/i18n";
import { XIcon } from "@/assets/icons/CrossIcon";
import { DangerIcon } from "@/assets/icons/DangerIcon";
import { CheckICon } from "@/assets/icons/CheckIcon";

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

const showToast = (message: string, icon: React.ReactNode, lang?: Lang) => {
  const currentLang = lang ?? getLocale();

  const content = (
    <div
      className={cn(
        "flex items-center gap-2 rounded-xl px-6",
        isRTL(currentLang) ? "text-left" : "flex-row-reverse  text-right",
        "text-xl font-bold text-text-base"
      )}
    >
      <div className={`!bg-none ${isRTL(currentLang) ? "order-1" : "order-2"}`}>
        {icon}
      </div>
      <div
        className={`leading-tight break-words ${
          isRTL(currentLang) ? "order-2" : "order-1"
        }`}
      >
        {message}
      </div>
    </div>
  );

  return toast(content, {
    ...baseOptions,
    classNames: {
      toast: `p-0 !bg-transparent !border-none backdrop-blur-md`,
    },
  });
};

export function Toaster({ className, ...props }: ToasterProps) {
  return <Sonner className={cn("toaster group", className)} {...props} />;
}

export const notify = {
  success: (message: string, lang?: Lang) =>
    showToast(
      message,
      <div className="size-12 rounded-full flex items-center justify-center bg-green-500">
        <CheckICon className="size-7 text-white" />
      </div>,
      lang
    ),

  error: (message: string, lang?: Lang) =>
    showToast(
      message,
      <div className="size-12 rounded-full flex items-center justify-center bg-red-500">
        <XIcon className="size-7 text-white" />
      </div>,
      lang
    ),

  warning: (message: string, lang?: Lang) =>
    showToast(
      message,
      <div className="size-12 rounded-full flex items-center justify-center bg-yellow-500">
      <DangerIcon className="size-7 text-white" />
    </div>,
      lang
    ),
};
