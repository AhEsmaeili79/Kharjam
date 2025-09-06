"use client"
import "./globals.css";

import { Button } from "@/components/ui/button";
import { ReactNode } from "react";
import Home from "./page";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-primary-100 size-full px-6">
            <h1 className="w-full text-base-100">desktop layout</h1>
            <main className="scrollbar">{children}</main>
          </body>
    </html>
  );
}
