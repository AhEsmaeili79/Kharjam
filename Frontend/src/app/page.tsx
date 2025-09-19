"use client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import "./globals.css";

const SplashScreenPage = () => {
  
  const router = useRouter();
  useEffect(() => {
    const timer = setTimeout(() => {
      router.push("/auth/login");
    }, 1000);
    return () => clearTimeout(timer);
  }, [router]);

  return (
    <html>
      <body>
        <div>
          <div className="auth-layout">
            <div className="size-32 bg-white rounded-[50%] flex items-center justify-center border border-primary-500 text-white"></div>
          </div>
        </div>
      </body>
    </html>
  );
};
export default SplashScreenPage;
