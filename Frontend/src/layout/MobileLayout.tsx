import BottomBar from "@/components/BottomBar";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";

const MobileLayout = ({ children }: { children: ReactNode }) => {
  const pathName = usePathname();
  return (
    <>
      <main className="w-full overflow-auto h-[calc(100%-70px)] scrollbar px-6 pb-16">
        {children}
      </main>
      {pathName === "/panel/dashboard" ? <BottomBar /> : <></>}
    </>
  );
};
export default MobileLayout;
