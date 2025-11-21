import { useMutation } from "@tanstack/react-query";
import * as api from "./api";
import type {
  RequestOTPRequest,
  VerifyOTPRequest,
  RefreshRequest,
} from "./api.schemas";
import { setTokens, clearTokens, getRefreshToken } from "@/lib/tokenManager";

const authApi = api.getUserService();

export const RequestOtpApiController = (identifier: string, router: any) =>
  useMutation({
    mutationFn: () =>
      // authApi.requestOtpApi({ identifier }).then((res: any) => {
      //   if (typeof window !== "undefined") {
      //     window.alert(res.data.message);
      //     localStorage.setItem("identifier", identifier);
      //   }
      //   router.push("/auth/otp");
      // }),
      router.push("/auth/otp")

  });

export const VerifyOtpApiController = (
  verifyOtp: VerifyOTPRequest,
  router: any
) =>
  useMutation({
    mutationFn: () =>
      authApi.verifyOtpApi(verifyOtp).then((res: any) => {
        // ذخیره token‌ها بعد از لاگین موفق
        const { access_token, refresh_token } = res.data;
        setTokens(access_token, refresh_token);
        
        if (typeof window !== "undefined") {
          window.alert(res.data.message);
          localStorage.removeItem("identifier");
        }
        router.push("/panel");
      }),
  });

export const RefreshTokenApiController = () =>
  useMutation({
    mutationFn: (payload: RefreshRequest) => authApi.refreshTokenApi(payload),
    onSuccess: (res) => {
      // ذخیره token‌های جدید بعد از refresh موفق
      const { access_token, refresh_token } = res.data;
      setTokens(access_token, refresh_token);
    },
  });

export const LogoutApiController = (router?: any) =>
  useMutation({
    mutationFn: async () => {
      const refreshToken = getRefreshToken();
      if (refreshToken) {
        try {
          await authApi.logoutApi({ refresh_token: refreshToken });
        } catch (error) {
          // حتی اگر logout در backend ناموفق بود، token‌ها را پاک می‌کنیم
          console.error("Logout error:", error);
        }
      }
      // پاک کردن token‌ها از localStorage
      clearTokens();
      // هدایت به صفحه لاگین
      if (router) {
        router.push("/auth/login");
      } else if (typeof window !== "undefined") {
        window.location.href = "/auth/login";
      }
    },
  });
