"use client";

import { useThemeStore } from "@/store/useThemeStore";

const ToggleThemeComponent = () => {
  const { dark, toggleTheme } = useThemeStore();

  return (
    <div
      className={`size-10 p-2 rounded-full flex items-center justify-center bg-sky-300 cursor-pointer shadow-md`}
      onClick={toggleTheme}
    >
      {dark ? "☀️" : "🌙"}
    </div>
  );
};

export default ToggleThemeComponent;
