import { useRouter } from "next/navigation";
import { useEffect } from "react";

const SplashScreenIndex = () =>{
    const router = useRouter();
    useEffect(() => {
      const timer = setTimeout(() => {
        router.push("/auth/login");
      }, 1000);
      return () => clearTimeout(timer);
    }, [router]);
    return(
        
<div>
      <div className="auth-layout">
        <div className="size-32 bg-white rounded-[50%] flex items-center justify-center border border-primary-500 text-white"></div>
      </div>
    </div>
    
    )
}

export default SplashScreenIndex