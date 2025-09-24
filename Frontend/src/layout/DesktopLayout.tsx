import { ReactNode } from "react"

const DesktopLayout = ({ children }: { children: ReactNode }) => {

    return (
        <main className="scrollbar">
            <h1 className="w-full ">desktop layout</h1>
            {children}
        </main>
    )
}
export default DesktopLayout