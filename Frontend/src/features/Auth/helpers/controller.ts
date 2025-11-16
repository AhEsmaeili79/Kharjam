import { useMutation } from "@tanstack/react-query";
import * as api from "./api";
import type {
  RequestOTPRequest,
  VerifyOTPRequest,
  RefreshRequest,
} from "./api.schemas";

const authApi = api.getUserService();

export const RequestOtpApiController = (identifier: string, router: any) =>
  useMutation({
    mutationFn: () =>
      authApi.requestOtpApi({ identifier }).then((res: any) => {
        window.alert(res.data.message);
        router.push("/auth/otp");
        localStorage.setItem("identifier", identifier);
      }),
  });

export const VerifyOtpApiController = (
  verifyOtp: VerifyOTPRequest,
  router: any
) =>
  useMutation({
    mutationFn: () =>
      authApi.verifyOtpApi(verifyOtp).then((res: any) => {
        console.log(res);
        window.alert(res.data.message)
        localStorage.removeItem("identifier");
        router.push("/panel");
      }),
  });

export const RefreshTokenApiController = () =>
  useMutation({
    mutationFn: (payload: RefreshRequest) => authApi.refreshTokenApi(payload),
  });

export const LogoutApiController = () =>
  useMutation({
    mutationFn: (payload: RefreshRequest) => authApi.logoutApi(payload),
  });
