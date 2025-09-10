import { useIsMobile } from "@/utils/useIsMobile"
import DesktopLayout from "./DesktopLayout"
import MobileLayout from "./MobileLayout"
import { ReactNode } from "react";

const ResponsiveLayout = ({ children }: { children: ReactNode }) => {
    const isMobile = useIsMobile();

    return (
        <>
            {isMobile ? (
                <MobileLayout>{children}</MobileLayout>
            ) : (
                <DesktopLayout>{children}</DesktopLayout>
            )}
        </>

    )
}
export default ResponsiveLayout