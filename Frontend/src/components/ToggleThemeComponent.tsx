"use client";

import { MoonIcon } from "@/assets/icons/MoonIcon";
import { SunIcon } from "@/assets/icons/SunIcon";
import { useThemeStore } from "@/store/useThemeStore";

const ToggleThemeComponent = () => {
  const { dark, toggleTheme } = useThemeStore();

  return (
    <div
      className={`size-10 p-2 rounded-full flex items-center justify-center bg-sky-100 dark:bg-sky-900 cursor-pointer shadow-md transition-colors hover:bg-sky-200/50 hover:dark:bg-sky-900/50`}
      onClick={toggleTheme}
    >
      {dark ? <SunIcon className="size-6 stroke-text-base"/> : <MoonIcon className="size-6 stroke-sky-500"/>}
    </div>
  );
};

export default ToggleThemeComponent;
