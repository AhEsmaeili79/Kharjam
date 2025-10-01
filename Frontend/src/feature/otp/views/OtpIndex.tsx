import { Button } from "@/components/ui/button";
import { InputOTP, InputOTPSlot } from "@/components/ui/input-otp";
import { useRouter } from "next/navigation";

const OtpIndex = () => {
  const router = useRouter();
  return (
    <div>
      <div className="flex flex-col justify-center items-center">
        <div className="character">
          <img src="/character.png" alt="character" className="size-40" />
        </div>
        <p className="mt-4 text-3xl text-text-base font-bold">Enter OTP code</p>
        <p className="mt-1 mb-4 text-text-secondary text-sm font-medium">
          Please enter the code sent to your phone
        </p>
        <div className=" my-8">
          <InputOTP
            autoFocus
            maxLength={6}
            onChange={(value) => console.log(value)}
          >
            <InputOTPSlot index={0} />
            <InputOTPSlot index={1} />
            <InputOTPSlot index={2} />
            <InputOTPSlot index={3} />
            <InputOTPSlot index={4} />
            <InputOTPSlot index={5} />
          </InputOTP>
          <p className=" text-center mt-4 text-text-secondary">
            Resend code 00:20
          </p>
        </div>
      </div>
      <div className="w-full flex flex-col items-center justify-center mt-20">
        <Button
          onClick={() => router.push("/panel")}
          className="h-12 px-10 bg-sky-400 hover:bg-sky-500 text-white font-bold rounded-full shadow-md"
        >
          Login
        </Button>
      </div>
    </div>
  );
};

export default OtpIndex;
