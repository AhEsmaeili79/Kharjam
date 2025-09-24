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
      <div className="character">
          <img src="/character.png" alt="character" className="size-40" />
        </div>
      </div>
    </div>
    
    )
}

export default SplashScreenIndex