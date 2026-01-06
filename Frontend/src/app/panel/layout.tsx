"use client";

import { ReactNode, useEffect } from "react";
import { NextIntlClientProvider } from "next-intl";
import { useLocale } from "@/utils/useLocaleUtil";
import "../globals.css";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/tokenManager";
import ToggleThemeComponent from "@/components/ToggleThemeComponent";
import ChangeLocaleComponent from "@/components/ChangeLocaleComponent";
import MobileLayout from "@/layout/MobileLayout";

export default function PanelLayout({ children }: { children: ReactNode }) {
  const { mounted, currentLocale, messages } = useLocale();
  const router = useRouter();

  useEffect(() => {
    if (mounted && !isAuthenticated()) {
      router.replace("/auth/login");
    }
  }, [mounted, router]);


  return (
    <NextIntlClientProvider locale={currentLocale} messages={messages}>
      <div className="auth-layout">
      <div className="absolute top-5 right-5">
          <ToggleThemeComponent />
        </div>
        <div className="absolute top-5 left-5">
          <ChangeLocaleComponent />
        </div>
        {mounted && <MobileLayout>{children}</MobileLayout>}
        {/* {mounted && <ResponsiveLayout>{children}</ResponsiveLayout>} */}
      </div>
    </NextIntlClientProvider>
  );
}
