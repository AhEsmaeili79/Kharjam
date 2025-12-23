import { useMutation } from "@tanstack/react-query";
import * as api from "./api";
import type { VerifyOTPRequest, RefreshRequest } from "./api.schemas";
import { setTokens, clearTokens, getRefreshToken } from "@/lib/tokenManager";
import { notify } from "@/components/ui/sonner";

const authApi = api.getUserService();

export const RequestOtpApiController = (identifier: string, router: any) =>
  useMutation({
    mutationFn: () => authApi.requestOtpApi({ identifier }),
    onSuccess: (res: any) => {
      if (typeof window !== "undefined") {
        notify.success(res.data.message);
        localStorage.setItem("identifier", identifier);
      }
      router.push("/auth/otp");
    },
    onError: (err: any) => {
      notify.error(err.message);
    },
  });

export const VerifyOtpApiController = (
  verifyOtp: VerifyOTPRequest,
  router: any
) =>
  useMutation({
    mutationFn: () => authApi.verifyOtpApi(verifyOtp),
    onSuccess: (res: any) => {
      const { access_token, refresh_token } = res.data;
      setTokens(access_token, refresh_token);
      router.push("/panel");
      notify.success('')
      if (typeof window !== "undefined") {
        localStorage.removeItem("identifier");
      }
    },
    onError: (err: any) => {
      notify.error(err.message);
    },
  });

export const RefreshTokenApiController = () =>
  useMutation({
    mutationFn: (payload: RefreshRequest) => authApi.refreshTokenApi(payload),
    onSuccess: (res) => {
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
          console.error("Logout error:", error);
        }
      }
      clearTokens();
      if (router) {
        router.push("/auth/login");
      } else if (typeof window !== "undefined") {
        window.location.href = "/auth/login";
      }
    },
  });
