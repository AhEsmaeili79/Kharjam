import axios from "axios";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_FETCH_AUTH_URL || "http://142.132.235.227:8001";

export const axiosBase = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});
