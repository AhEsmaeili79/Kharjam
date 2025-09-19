"use client";

import { ReactNode } from "react";
import { NextIntlClientProvider } from "next-intl";
import { useLocale } from "@/utils/useLocaleUtil";
import ResponsiveLayout from "@/layout/ResponsiveLayout";
import "../globals.css";

export default function PanelLayout({ children }: { children: ReactNode }) {
  const { mounted, currentLocale, messages } = useLocale();

  return (
    <NextIntlClientProvider locale={currentLocale} messages={messages}>
      <div
        className="bg-primary-100 w-full h-screen px-6"
        suppressHydrationWarning
      >
        {mounted ? (
          <ResponsiveLayout>{children}</ResponsiveLayout>
        ) : (
          <div />
        )}
      </div>
    </NextIntlClientProvider>
  );
}
