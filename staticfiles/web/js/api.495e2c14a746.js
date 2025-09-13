import axios from "https://cdn.skypack.dev/axios@1.6.2";

export const API = axios.create({
  baseURL: "/api/v1/",
});

/* attach JWT on each request */
API.interceptors.request.use(cfg => {
  const token = localStorage.getItem("access");
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});

/* handle token refresh and expired tokens */
API.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // If the error is 401 (Unauthorized) and we haven't already tried to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem("refresh");
      
      if (refreshToken) {
        try {
          // Try to refresh the token
          const response = await axios.post("/api/v1/auth/refresh/", {
            refresh: refreshToken
          });
          
          const { access } = response.data;
          
          // Update the stored access token
          localStorage.setItem("access", access);
          
          // Update the original request with the new token
          originalRequest.headers.Authorization = `Bearer ${access}`;
          
          // Retry the original request
          return API(originalRequest);
        } catch (refreshError) {
          // If refresh fails, clear all tokens and redirect to login
          console.error("Token refresh failed:", refreshError);
          localStorage.clear();
          window.location.href = "/login/";
          return Promise.reject(refreshError);
        }
      } else {
        // No refresh token available, redirect to login
        localStorage.clear();
        window.location.href = "/login/";
        return Promise.reject(error);
      }
    }
    
    // For other errors, just pass them through
    return Promise.reject(error);
  }
);
