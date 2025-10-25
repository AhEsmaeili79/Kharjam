// import axios from "axios";

// const instance = axios.create({
//   baseURL: process.env.NEXT_PUBLIC_AUTH_BASE_URL || "http://142.132.235.227:8001",
//   headers: {
//     "Content-Type": "application/json",
//   },
// });

// export const axiosInstance = <TData = unknown>(config: any) => {
//   return instance(config);
// };


import axios, { AxiosRequestConfig } from "axios";

// === 🔧 Base URL ===
const API_BASE_URL =
  process.env.NEXT_PUBLIC_AUTH_BASE_URL || "http://142.132.235.227:8001";

// === 🔐 Token Helpers ===
function getAccessToken() {
  if (typeof window !== "undefined") {
    return localStorage.getItem("access_token");
  }
  return null;
}

function getRefreshToken() {
  if (typeof window !== "undefined") {
    return localStorage.getItem("refresh_token");
  }
  return null;
}

function setTokens(access: string, refresh: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
  }
}

// === 🧱 Create Axios Instance ===
const instance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// === 📨 Request Interceptor ===
instance.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) {
      config.headers = config.headers || {};
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// === 🔁 Response Interceptor (Token Refresh) ===
instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      getRefreshToken()
    ) {
      originalRequest._retry = true;
      try {
        const refreshToken = getRefreshToken();
        const res = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
          refresh: refreshToken,
        });

        const { access, refresh } = res.data;
        setTokens(access, refresh);

        instance.defaults.headers["Authorization"] = `Bearer ${access}`;
        originalRequest.headers["Authorization"] = `Bearer ${access}`;

        return instance(originalRequest);
      } catch (refreshError) {
        if (typeof window !== "undefined") {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          // Optionally: window.location.href = '/auth/login';
        }
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// === ⚙️ Exported Mutator for Orval ===
export const axiosInstance = <TData = unknown>(config: AxiosRequestConfig) => {
  return instance(config);
};
