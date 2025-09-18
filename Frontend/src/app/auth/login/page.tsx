"use client";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

const LoginPage = () => {
  const router = useRouter();

  return (
    <div>
      <div className="flex flex-col justify-center items-center">
        <div className="size-32 bg-white rounded-[50%] flex items-center justify-center border border-primary-500 text-white"></div>
        <p className="mt-4 text-3xl text-primary-700 font-bold">
          welcome, friend!
        </p>
        <p className="mt-1 mb-4 text-primary-600 text-sm font-bold">
          welcome back, login to continue
        </p>
        <input
          type="text"
          className="h-10 border border-primary-300 rounded-lg px-3 flex items-center"
          placeholder="username"
        />
      </div>
      <div className="w-full flex flex-col items-center justify-center mt-20">
        <Button className="flex items-center gap-3 px-6 py-3 bg-white text-gray-800 font-medium rounded-full shadow-md mb-4">
          <img src="/google-icon.svg" alt="Google" className="w-6 h-6" />
          <span>Sign in with Google</span>
        </Button>
        <Button
          onClick={() => router.push("/auth/otp")}
          className="px-10 py-3 bg-sky-400 text-white font-bold rounded-full shadow-md"
        >
          send code
        </Button>
      </div>
    </div>
  );
};

export default LoginPage;
