"use client";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

const LoginPage = () => {
  const router = useRouter();

  return (
    <div className="w-full">
      <div className="flex flex-col justify-center items-center">
        <div className="bg-[#fefefe] rounded-[50%] flex items-center justify-center border border-primary-500">
          <img src="/character.png" alt="character" className="size-40" />
        </div>
        <p className="mt-4 text-3xl text-primary-700 font-bold">Welcome, friend!</p>
        <p className="mt-1 mb-4 text-primary-600 text-sm font-medium">
          Welcome back, please log in to continue.
        </p>
        <div className="w-full relative flex justify-center">
          <div className="size-6 absolute bg-sky-200 rounded-full right-12 top-1/2 -translate-y-1/2"></div>
          <input
            type="text"
            inputMode="email"
            autoComplete="email tel"
            aria-label="Email or Phone Number"
            className="h-14 w-10/12 border rounded-xl px-4 outline-none bg-white border-sky-500 focus:border-sky-700 focus:ring-2 focus:ring-sky-200 transition"
            placeholder="Email or Phone Number"
          />
        </div>
      </div>
      <div className="w-full flex flex-col items-center justify-center mt-32">
        <Button
          variant="outline"
          className="h-11 flex items-center gap-3 px-6 bg-white text-gray-800 rounded-full shadow-sm mb-4"
        >
          <img src="/google-icon.svg" alt="Google" className="w-6 h-6" />
          <span>Sign in with Google</span>
        </Button>
        <Button
          onClick={() => router.push("/auth/otp")}
          className="h-12 px-10 bg-sky-400 hover:bg-sky-500 text-white font-bold rounded-full shadow-md"
        >
          Login
        </Button>
      </div>
    </div>
  );
};

export default LoginPage;
