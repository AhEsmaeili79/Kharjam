import "./globals.css";
import type { Metadata } from "next";
import { defaultLocale } from "@/i18n";
import Providers from "./providers";
import { Toaster } from "@/components/ui/sonner";
import { Baloo_Bhaijaan_2 } from "next/font/google";
import { Outfit } from "next/font/google";
import ThemeInitializer from "@/components/ThemeInitializer";

export const metadata: Metadata = {
  title: "Kharjam",
  description: "split expenses with friends",
  icons: {
    icon: "/logo.png",
  },
};

const baloo = Baloo_Bhaijaan_2({
  subsets: ["arabic"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-baloo",
});

const Nunito = Outfit({
  subsets: ["latin"],
  variable: "--font-Nunito",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang={defaultLocale}
      dir={defaultLocale === "fa" ? "rtl" : "ltr"}
    >
      <body className={`${baloo.variable} ${Nunito.variable}`}>
        <ThemeInitializer />
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
