"use client";
import { axiosBase, API_BASE_URL } from "./axiosBase";
import axios, { AxiosRequestConfig } from "axios";
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from "./tokenManager";

const axiosClient = axiosBase;

// Request interceptor: اضافه کردن access token به header
axiosClient.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers = config.headers || {};
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: مدیریت refresh token
axiosClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const refreshToken = getRefreshToken();

    // اگر خطای 401 دریافت شد و refresh token وجود دارد و درخواست قبلاً retry نشده
    if (
      error.response &&
      error.response.status === 401 &&
      refreshToken &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      try {
        // درخواست refresh token
        const res = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token, refresh_token } = res.data;
        
        // ذخیره token‌های جدید
        setTokens(access_token, refresh_token);

        // به‌روزرسانی header درخواست اصلی
        originalRequest.headers["Authorization"] = `Bearer ${access_token}`;

        // ارسال مجدد درخواست اصلی با token جدید
        return axiosClient(originalRequest);
      } catch (refreshError) {
        // اگر refresh token نامعتبر بود، token‌ها را پاک کن و به صفحه لاگین هدایت کن
        clearTokens();
        
        // اگر در صفحه لاگین نیستیم، به صفحه لاگین هدایت می‌کنیم
        if (typeof window !== "undefined" && !window.location.pathname.includes("/auth")) {
          window.location.href = "/auth/login";
        }
        
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const axiosInstance = <TData = unknown>(config: AxiosRequestConfig) =>
  axiosClient(config);

export default axiosClient;
