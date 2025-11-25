"use client";

import ChangeLocaleComponent from "@/components/ChangeLocaleComponent";
import ToggleThemeComponent from "@/components/ToggleThemeComponent";
import { Button } from "@/components/ui/button";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";

export default function Home() {
  const t = useTranslations();
  const [dark, setDark] = useState(false);
  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [dark]);

  return (
    <div className="flex-col">
      <div className="w-full flex justify-end">
      main
       <ChangeLocaleComponent/>
      <ToggleThemeComponent/>
      </div>
    </div>
  );
}