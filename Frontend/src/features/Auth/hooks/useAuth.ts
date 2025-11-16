import * as controller from "../helpers/controller";
import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { isAuthenticated } from "@/lib/tokenManager";
import { notify } from "@/components/ui/sonner";
import { useLocaleStore } from "@/store/useLocaleStore";

export const useAuth = () => {
  const t = useTranslations();
  const router = useRouter();
  const [identifier, setIdentifier] = useState<string>("");
  const [authStatus, setAuthStatus] = useState<boolean>(false);

  const [verifyOtp, setVerifyOtp] = useState({
    identifier: "",
    otp_code: "",
  });

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


    const locale = useLocaleStore((state) => state.locale);
    const persianArabicRegex = /[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]/;
  
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      let value = e.target.value;
      if (value === "") {
        setIdentifier("");
        return;
      }
      if (persianArabicRegex.test(value)) {
        notify.warning(t("login-input-error-keyboard"), locale as "fa" | "en");
        return;
      }
      const allowedChars = /^[a-zA-Z0-9@._%+-]+$/;
      if (!allowedChars.test(value)) {
        notify.warning(t("login-input-error-keyboard"), locale as "fa" | "en");
        return;
      }
  
      if (value.includes("@")) {
        setIdentifier(value);
        return;
      }
  
      if (/^\d+$/.test(value)) {
        if (value.startsWith("0") && value.length > 1) {
          value = "98" + value.slice(1);
        }
        setIdentifier(value);
        return;
      }
      setIdentifier(value);
    };




    const [otpValue, setOtpValue] = useState(verifyOtp.otp_code);
    useEffect(() => {
      setOtpValue(verifyOtp.otp_code);
    }, [verifyOtp.otp_code]);
  
    const handleOtpChange = useCallback((value: string) => {
      const numericValue = value.replace(/\D/g, '');
      const limitedValue = numericValue.slice(0, 6);
      setOtpValue(limitedValue);
      setVerifyOtp((prev) => ({
        ...prev,
        otp_code: limitedValue,
      }));
    }, [setVerifyOtp]);
  

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
    handleInputChange,
    handleOtpChange,
    otpValue
  };
};
