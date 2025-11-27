import BottomBar from "@/components/BottomBar";
import { ReactNode } from "react";

const MobileLayout = ({ children }: { children: ReactNode }) => {
  return (
    <>
      <main className="w-full overflow-auto h-[calc(100%-70px)] scrollbar px-6 pb-16">
        {children}
      </main>
      <BottomBar />
    </>
  );
};
export default MobileLayout;
