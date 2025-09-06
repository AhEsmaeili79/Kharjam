"use client"
import BottomBar from "@/components/BottomBar";
import "./globals.css";
import { ReactNode, useEffect, useState } from "react";
import { Home, Search, PlusCircle, Bell, User } from "lucide-react";


export default function RootLayout({ children }: { children: ReactNode }) {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < 768);
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

  return (
    <html lang="en">
      {
        isMobile ?
          <body className="w-full h-screen bg-primary-100 overflow-none">
            <div className="w-full h-12 flex justify-between items-center px-6">
              <div>
                <span>lang</span>
                <span>theme</span>
              </div>
              <div className="size-8 rounded-full bg-amber-500 flex items-center justify-center"><User size={22} /></div>
            </div>
            <main className="overflow-auto h-[calc(100%-70px)] scrollbar px-6">{children}</main>
            <BottomBar />

          </body>
          :
          <body className="bg-primary-100 size-full px-6">
            <h1 className="w-full text-base-100">desktop layout</h1>
            <main className="scrollbar">{children}</main>
          </body>
      }
    </html>
  );
}