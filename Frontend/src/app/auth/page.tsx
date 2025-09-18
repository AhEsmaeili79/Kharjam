"use client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
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
          <div className="flex flex-col justify-center items-center">
            <div className="size-32 bg-white rounded-[50%] flex items-center justify-center border border-primary-500 text-white"></div>
            <p className="mt-10 text-primary-700">splash screen</p>
          </div>
        </div>
      </body>
    </html>
  );
};
export default SplashScreenPage;
