import "./globals.css";
import type { Metadata } from "next";
import { defaultLocale } from "@/i18n";

export const metadata: Metadata = {
  title: "Kharjam",
  description: "split expenses with friends",
  icons: {
    icon: "/logo.png", // must be inside /public
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang={defaultLocale} dir={defaultLocale === "fa" ? "rtl" : "ltr"}>
      <body>{children}</body>
    </html>
  );
}
