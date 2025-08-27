// "use_client"
import "./globals.css";
// import { Button } from "@/components/ui/button"
// import Home from './home/page';

import { Button } from "@/components/ui/button";
import { ReactNode } from "react";
import Home from "./page";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-500 size-full">
        <h1 className="text-green-600">the layout</h1>
        <main className="p-4">{children}</main>
        <div></div>
      </body>
    </html>
  );
}
