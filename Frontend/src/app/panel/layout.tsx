"use client";

import { ReactNode } from "react";
import { NextIntlClientProvider } from "next-intl";
import { defaultLocale } from "@/i18n";
import "../globals.css";
import { useLocale } from "@/utils/useLocaleUtil";
import ResponsiveLayout from "@/layout/ResponsiveLayout";

export default function RootLayout({ children }: { children: ReactNode }) {
  const { mounted, currentLocale, messages } = useLocale();

  return (
    <html lang={defaultLocale} dir={defaultLocale === "fa" ? "rtl" : "ltr"}>
      <body className="bg-primary-100 w-full h-screen px-6">
        <NextIntlClientProvider locale={currentLocale} messages={messages}>
          {mounted && (
            <ResponsiveLayout>{children}</ResponsiveLayout>
          )}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
