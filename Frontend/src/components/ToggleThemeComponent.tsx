"use client";

import { useThemeStore } from "@/store/useThemeStore";

const ToggleThemeComponent = () => {
    const { dark, toggleTheme } = useThemeStore();

    return (
        <div className="flex flex-col items-center justify-center">
            <button
                onClick={toggleTheme}
                className="px-4 py-2 rounded-lg text-white bg-accent-500"
            >
                {dark ? "☀️ Light Mode" : "🌙 Dark Mode"}
            </button>
        </div>
    );
}

export default ToggleThemeComponent
