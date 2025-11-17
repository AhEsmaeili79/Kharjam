/**
 * Token Manager Utility
 * مدیریت access token و refresh token
 */

const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

/**
 * دریافت access token از localStorage
 */
export const getAccessToken = (): string | null => {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(ACCESS_TOKEN_KEY);
};

/**
 * دریافت refresh token از localStorage
 */
export const getRefreshToken = (): string | null => {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

/**
 * ذخیره access token و refresh token در localStorage
 */
export const setTokens = (accessToken: string, refreshToken: string): void => {
  if (typeof window === "undefined") return;
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
};

/**
 * پاک کردن token‌ها از localStorage
 */
export const clearTokens = (): void => {
  if (typeof window === "undefined") return;
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

/**
 * بررسی اینکه آیا کاربر لاگین است یا نه
 */
export const isAuthenticated = (): boolean => {
  return !!getAccessToken() && !!getRefreshToken();
};

