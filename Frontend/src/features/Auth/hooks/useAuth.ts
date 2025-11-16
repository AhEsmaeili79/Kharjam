import * as controller from "../helpers/controller";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { isAuthenticated } from "@/lib/tokenManager";

export const useAuth = () => {
  const t = useTranslations();
  const router = useRouter();
  const [identifier, setIdentifier] = useState<string>("");
  const [authStatus, setAuthStatus] = useState<boolean>(false);

  const [verifyOtp, setVerifyOtp] = useState({
    identifier: "",
    otp_code: "",
  });

  // مقداردهی اولیه از localStorage فقط در سمت کلاینت
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedIdentifier = localStorage.getItem("identifier");
      if (savedIdentifier) {
        setVerifyOtp((prev) => ({
          ...prev,
          identifier: savedIdentifier,
        }));
      }
      setAuthStatus(isAuthenticated());
    }
  }, []);

  const { mutate: requestOtpMutate, isPending: requestOtpPending } =
    controller.RequestOtpApiController(identifier, router);

  const { mutate: verifyOtpMutate, isPending: verifyOtpPending } =
    controller.VerifyOtpApiController(verifyOtp, router);

  const { mutate: logoutMutate, isPending: logoutPending } =
    controller.LogoutApiController(router);

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
    logoutMutate,
    logoutPending,
    isAuthenticated: authStatus,
  };
};
