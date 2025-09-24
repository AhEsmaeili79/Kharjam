"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

const OtpPage = () => {
  const router = useRouter();
  const [values, setValues] = useState(["", "", "", "", "", ""]);
  const inputsRef = useRef<Array<HTMLInputElement | null>>([]);

  useEffect(() => {
    inputsRef.current[0]?.focus();
  }, []);

  const handleChange = (index: number, next: string) => {
    const digit = next.replace(/\D/g, "").slice(-1);
    const nextValues = [...values];
    nextValues[index] = digit ?? "";
    setValues(nextValues);
    if (digit && index < inputsRef.current.length - 1) {
      inputsRef.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace" && !values[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
  };
  return (
    <div>
      <div className="flex flex-col justify-center items-center">
        <img src="/character.png" alt="character" className="size-44" />
        <p className="mt-4 text-3xl text-primary-700 font-bold">
          Enter OTP code
        </p>
        <p className="mt-1 mb-4 text-primary-600 text-sm font-bold">
          Please enter the code sent to your phone
        </p>
        <div className=" my-8">
          <div className="mx-8 grid grid-cols-6 gap-3">
            {values.map((v, i) => (
              <input
                key={i}
                ref={(el) => {
                  inputsRef.current[i] = el;
                }}
                type="text"
                inputMode="numeric"
                autoComplete="one-time-code"
                maxLength={1}
                value={v}
                onChange={(e) => handleChange(i, e.target.value)}
                onKeyDown={(e) => handleKeyDown(i, e)}
                className="h-12 w-12 text-center text-lg border border-primary-300 rounded-lg mt-4 outline-none focus:border-sky-600 focus:ring-2 focus:ring-sky-200"
              />
            ))}
          </div>
          <p className=" text-center mt-4 ">Resend code 00:20</p>
        </div>
      </div>
      <div className="w-full flex flex-col items-center justify-center mt-20">
        <Button
        onClick={()=>router.push("/panel")}
        className="h-12 px-10 bg-sky-400 hover:bg-sky-500 text-white font-bold rounded-full shadow-md">
          Login
        </Button>
      </div>
    </div>
  );
};

export default OtpPage;
