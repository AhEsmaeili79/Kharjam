import "./globals.css";
import type { Metadata } from "next";
import { defaultLocale } from "@/i18n";
import Providers from "./providers";
import { Toaster } from "@/components/ui/sonner";

export const metadata: Metadata = {
  title: "Kharjam",
  description: "split expenses with friends",
  icons: {
    icon: "/logo.png",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang={defaultLocale} dir={defaultLocale === "fa" ? "rtl" : "ltr"}>
      <body>
         <Providers>
        {children}
        <Toaster
          position="top-center"
          richColors
          toastOptions={{
            duration: 3000,
          }}
        />
         </Providers>
        </body>
    </html>
  );
}
