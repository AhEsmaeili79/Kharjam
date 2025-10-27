import { Button } from "@/components/ui/button";
import { InputOTP, InputOTPSlot } from "@/components/ui/input-otp";
import { useTranslations } from "next-intl";
import { useRouter } from "next/navigation";

const OtpIndex = () => {
  const router = useRouter();
  const t = useTranslations()
  return (
    <div>
      <div className="flex flex-col justify-center items-center">
        <div className="character">
          <img src="/character.png" alt="character" className="size-40" />
        </div>
        <p className="mt-4 text-3xl text-text-base font-bold">{t("otp-text")}</p>
        <p className="mt-1 mb-4 text-text-secondary text-sm font-medium">
          {t("otp-subText")}
        </p>
        <div className=" my-8" dir="ltr">
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
          </InputOTP>
          <p className=" text-center mt-4 text-text-secondary">
            {t("otp-code")} 00:20
          </p>
        </div>
      </div>
      <div className="w-full flex flex-col items-center justify-center mt-20">
        <Button
          onClick={() => router.push("/panel")}
          className="h-12 px-10 bg-sky-400 hover:bg-sky-500 text-white font-bold rounded-full shadow-md"
        >
          {t("otp-btn")}
        </Button>
      </div>
    </div>
  );
};

export default OtpIndex;
