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

axiosClient.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers = config.headers || {};
    config.headers["Authorization"] = `Bearer ${token}`;
  }

  if (typeof window !== "undefined") {
    const locale = localStorage.getItem("locale") || "fa";
    config.headers = config.headers || {};
    config.headers["Accept-Language"] = locale;
  }

  return config;
});


axiosClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const refreshToken = getRefreshToken();

    if (
      error.response &&
      error.response.status === 401 &&
      refreshToken &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      try {
        const res = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token, refresh_token } = res.data;
        
        setTokens(access_token, refresh_token);

        
        originalRequest.headers["Authorization"] = `Bearer ${access_token}`;


        return axiosClient(originalRequest);
      } catch (refreshError) {
        clearTokens();
        
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
