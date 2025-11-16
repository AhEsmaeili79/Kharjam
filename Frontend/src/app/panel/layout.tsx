"use client";

import { ReactNode, useEffect } from "react";
import { NextIntlClientProvider } from "next-intl";
import { useLocale } from "@/utils/useLocaleUtil";
import ResponsiveLayout from "@/layout/ResponsiveLayout";
import "../globals.css";
import { useRouter } from "next/navigation";

function isAuthenticated() {
  if (typeof window !== "undefined") {
    return !!localStorage.getItem("access_token");
  }
  return false;
}

export default function PanelLayout({ children }: { children: ReactNode }) {
  const { mounted, currentLocale, messages } = useLocale();
  const router = useRouter();

  // useEffect(() => {
  //   if (mounted && !isAuthenticated()) {
  //     router.replace("/auth/login");
  //   }
  // }, [mounted, router]);

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
