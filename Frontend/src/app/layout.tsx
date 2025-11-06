import "./globals.css";
import type { Metadata } from "next";
import { defaultLocale } from "@/i18n";
import Providers from "./providers";

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
         </Providers>
        </body>
    </html>
  );
}
