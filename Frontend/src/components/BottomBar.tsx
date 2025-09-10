import React, { useState } from "react";
import { cn } from "@/lib/utils";
import { Home, Search, PlusCircle, Bell, User } from "lucide-react";

function BottomBar() {
    const [selected, setSelected] = useState("");
    const navItems = [
        { id: "home", label: "Home", icon: <Home size={22} /> },
        { id: "search", label: "Search", icon: <Search size={22} /> },
        { id: "add", label: "Add", icon: <PlusCircle size={22} /> },
        { id: "notifications", label: "Alerts", icon: <Bell size={22} /> },
        { id: "profile", label: "Profile", icon: <User size={22} /> },
    ];
    return (
        <div className="fixed bottom-0 w-full h-26 bg-transparent pointer-events-none">
            {/* Curved container */}
            <div className="fixed inset-x-0 bottom-0 h-16 bg-white rounded-t-3xl shadow-lg pointer-events-auto">
                <div className="relative h-full flex items-center justify-around">
                    {navItems.map((item) => {
                        const isSel = selected === item.id;
                        return (
                            <button
                                key={item.id}
                                onClick={() => setSelected(item.id)}
                                className={cn(
                                    "relative flex flex-col items-center justify-center transition-all duration-300 ease-out",
                                    isSel
                                        ? "-mt-8 bg-primary-500 text-white shadow-xl rounded-full w-16 h-16 animate-rebound"
                                        : "text-gray-500 hover:text-primary-500 w-12 h-12 hover:-translate-y-1"
                                )}
                                style={{ pointerEvents: "auto" }}
                            >
                                {item.icon}
                                <p>{item.label}</p>
                            </button>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}

export default BottomBar;