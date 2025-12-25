import * as controller from "../helpers/controller";
import { useState, useEffect, useCallback } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useLocale, useTranslations } from "next-intl";
import { isAuthenticated } from "@/lib/tokenManager";
import { notify } from "@/components/ui/sonner";
import { useLocaleStore } from "@/store/useLocaleStore";

export const useAuth = () => {
  const t = useTranslations();
  const router = useRouter();
  const locales = useLocale();
  const isRTL = locales === "fa";
  const [otpTimer,setOtpTimer] = useState<any>('')
  const [identifier, setIdentifier] = useState<string>("");
  const [authStatus, setAuthStatus] = useState<boolean>(false);
  const pathName = usePathname();
  const [verifyOtp, setVerifyOtp] = useState({
    identifier: "",
    otp_code: "",
  });
  const [otpValue, setOtpValue] = useState(verifyOtp.otp_code);

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

      if (pathName === "/auth/otp") {
        // On OTP page, ensure timer starts if not already running
        const existingTimer = localStorage.getItem('otp-timer');
        if (!existingTimer) {
          localStorage.setItem('otp-timer', (3 * 60).toString());
        }
        setOtpTimer(localStorage.getItem('otp-timer'));
      } else {
        localStorage.removeItem("otp-timer");
      }

      // Poll for localStorage changes every second
      const interval = setInterval(() => {
        const currentTimer = localStorage.getItem('otp-timer');
        setOtpTimer(currentTimer);
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [pathName]);

  const { mutate: requestOtpMutate, isPending: requestOtpPending } =
    controller.RequestOtpApiController(identifier, router);

  const { mutate: verifyOtpMutate, isPending: verifyOtpPending } =
    controller.VerifyOtpApiController(verifyOtp, router);

  const { mutate: logoutMutate, isPending: logoutPending } =
    controller.LogoutApiController(router);

  const locale = useLocaleStore((state) => state.locale);
  const persianArabicRegex =
    /[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]/;

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

  useEffect(() => {
    setOtpValue(verifyOtp.otp_code);
  }, [verifyOtp.otp_code]);

  const handleOtpChange = useCallback(
    (value: string) => {
      const numericValue = value.replace(/\D/g, "");
      const limitedValue = numericValue.slice(0, 6);
      setOtpValue(limitedValue);
      setVerifyOtp((prev) => ({
        ...prev,
        otp_code: limitedValue,
      }));
    },
    [setVerifyOtp]
  );

  const requestOtpEnterHandler = (e: any) => {
    if (e.key === "Enter" && identifier !== "" && !requestOtpPending) {
      requestOtpMutate();
    }
  };

  const verifyOtpEnterHandler = (e: any) => {
    if (
      e.key === "Enter" &&
      verifyOtp.otp_code.length == 5 &&
      !verifyOtpPending
    ) {
      verifyOtpMutate();
    }
  };

  const handleResendOtp = () => {
    localStorage.setItem('otp-timer', (3 * 60).toString());
    requestOtpMutate();
  };

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
    otpValue,
    isRTL,
    requestOtpEnterHandler,
    verifyOtpEnterHandler,
    otpTimer,
    handleResendOtp
  };
};
