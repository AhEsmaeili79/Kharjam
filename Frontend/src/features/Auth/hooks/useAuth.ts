import * as controller from "../helpers/controller";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";


export const useAuth = () => {
  const t = useTranslations();
  const router = useRouter();
  const [identifier, setIdentifier] = useState<string>("");

  const [verifyOtp, setVerifyOtp] = useState({
    identifier: localStorage.getItem('identifier') ?? '',
    otp_code: "",
  });

  const { mutate: requestOtpMutate, isPending: requestOtpPending } =
    controller.RequestOtpApiController(identifier, router);

  const { mutate: verifyOtpMutate, isPending: verifyOtpPending } =
    controller.VerifyOtpApiController(verifyOtp, router);

  return {
    t,
    router,
    verifyOtp,
    identifier,
    setVerifyOtp,
    setIdentifier,
    verifyOtpMutate,
    requestOtpMutate,
    requestOtpPending,
    verifyOtpPending,
  };
};
