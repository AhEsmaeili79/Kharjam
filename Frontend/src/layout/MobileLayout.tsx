import BottomBar from "@/components/BottomBar";
import { User } from "lucide-react";
import { ReactNode } from "react";

const MobileLayout = ({ children }: { children: ReactNode }) => {
  return (
    <>
      <div className="w-full h-12 flex justify-between items-center px-6">
        <div>
          <span>lang</span>
          <span>theme</span>
        </div>
        <div className="size-8 rounded-full bg-amber-500 flex items-center justify-center">
          <User size={22} />
        </div>
      </div>
      <main className="overflow-auto h-[calc(100%-70px)] scrollbar px-6 pb-16">
        {children}
      </main>
      <BottomBar />
    </>
  );
};
export default MobileLayout;
