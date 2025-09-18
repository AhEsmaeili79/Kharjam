"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

const OtpPage = () => {
   const router = useRouter();
  return (
    <div>
      <div className="flex flex-col justify-center items-center">
        <div className="size-32 bg-white rounded-[50%] flex items-center justify-center border border-primary-500 text-white"></div>
        <p className="mt-4 text-3xl text-primary-700 font-bold">
          enter otp code
        </p>
        <p className="mt-1 mb-4 text-primary-600 text-sm font-bold">
          please enter the code sent to your phone
        </p>
        <div className=" my-8">
          <div className="mx-8 grid grid-cols-5 gap-4">
            <input
              type="text"
              className="h-10 border border-primary-300 rounded-lg mt-4 px-3 flex items-center"
            />
            <input
              type="text"
              className="h-10 border border-primary-300 rounded-lg mt-4 px-3 flex items-center"
            />
            <input
              type="text"
              className="h-10 border border-primary-300 rounded-lg mt-4 px-3 flex items-center"
            />
            <input
              type="text"
              className="h-10 border border-primary-300 rounded-lg mt-4 px-3 flex items-center"
            />
            <input
              type="text"
              className="h-10 border border-primary-300 rounded-lg mt-4 px-3 flex items-center"
            />
          </div>
          <p className=" text-center mt-4 text-base-500">resend code 00:20</p>
        </div>
      </div>
      <div className="w-full flex flex-col items-center justify-center mt-20">
        <Button
        onClick={()=>router.push("/panel")}
        className="px-10 py-3 bg-sky-400 text-white font-bold rounded-full shadow-md">
          login
        </Button>
      </div>
    </div>
  );
};

export default OtpPage;
