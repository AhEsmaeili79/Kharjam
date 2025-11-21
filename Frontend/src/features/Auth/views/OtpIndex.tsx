import { Button } from "@/components/ui/button";
import { InputOTP, InputOTPSlot } from "@/components/ui/input-otp";
import { useAuth } from "../hooks/useAuth";
import Timer from "@/components/Timer";

const OtpIndex = () => {
  const {
    t,
    verifyOtp,
    verifyOtpMutate,
    verifyOtpPending,
    handleOtpChange,
    otpValue,
    isRTL
  } = useAuth();
 

  return (
    <div>
      <div className="flex flex-col justify-center items-center">
        <div className="character">
          <img src="/character.png" alt="character" className="size-40" />
        </div>
        <p className="mt-4 text-3xl text-text-base font-bold">
          {t("otp-text")}
        </p>
        <p className="mt-1 mb-4 text-text-secondary text-sm font-medium">
          {t("otp-subText")}
        </p>
        <div className=" my-8" dir="ltr">
          <InputOTP
            autoFocus
            maxLength={6}
            value={otpValue}
            onChange={handleOtpChange}
          >
            <InputOTPSlot index={0} />
            <InputOTPSlot index={1} />
            <InputOTPSlot index={2} />
            <InputOTPSlot index={3} />
            <InputOTPSlot index={4} />
            <InputOTPSlot index={5} />
          </InputOTP>
          <div
            className={`w-full flex items-center justify-center gap-3 mt-4 text-text-secondary ${
              isRTL ? " flex-row" : "flex-row-reverse"
            }`}
          >
            <Timer storageKey="otp-timer" minutes={3} />
            <p className="whitespace-nowrap">{t("otp-code")}</p>
          </div>
        </div>
      </div>
      <div className="w-full flex flex-col items-center justify-center mt-20">
        <Button
          disabled={verifyOtpPending || verifyOtp.otp_code.length < 5}
          onClick={() => {
            verifyOtpMutate();
          }}
          className="h-12 px-10 bg-sky-400 hover:bg-sky-500 text-white font-bold rounded-full shadow-md"
        >
          {t("otp-btn")}
        </Button>
      </div>
    </div>
  );
};

export default OtpIndex;
