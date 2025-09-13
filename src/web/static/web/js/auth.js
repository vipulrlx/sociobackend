import { API } from "./api.js";

/* call backend, store tokens + user payload */
export async function login(email, password) {
  const { data } = await API.post("auth/login/", { email, password });
  persistUser(data);
  return data.user;
}

export async function register(payload) {
  try {
    const { data } = await API.post("auth/register/", payload);
    persistUser(data);
    return data.user;
  } catch (error) {
    // Handle the new error response structure
    if (error.response?.data?.message) {
      throw new Error(error.response.data.message);
    } else if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    } else {
      throw new Error("Registration failed. Please try again.");
    }
  }
}

export async function googleSessionLogin(credential) {
  if (!credential) throw new Error("Missing Google credential");
  const r = await fetch("/api/v1/auth/google/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",          // <-- store the session cookie
    body: JSON.stringify({ credential: credential })
  });
  const data = await r.json();
  console.log(data)
  persistUser(data);
  return data.user;
}

// export async function googleLogin(id_token) {
//   console.log("Google login called with token:", id_token ? id_token.substring(0, 50) + "..." : "null");
//   try {
//     const { data } = await API.post("auth/google/", { id_token });
//     console.log("Google login response:", data);
//     persistUser(data);
//     return data.user;
//   } catch (error) {
//     console.error("Google login API error:", error);
//     console.error("Error response:", error.response?.data);
//     throw error;
//   }
// }

export function logout() {
  const refresh = localStorage.getItem("refresh");
  if (refresh) {
    API.post("auth/logout/", { refresh }).catch(() => {
      // Even if logout API fails, clear local storage
      console.log("Logout API failed, clearing local storage anyway");
    });
  }
  localStorage.clear();
  location.href = "/logout/";
}

/* Check if user is authenticated */
export function isAuthenticated() {
  const access = localStorage.getItem("access");
  const refresh = localStorage.getItem("refresh");
  return !!(access && refresh);
}

/* Get current user data */
export function getCurrentUser() {
  const userStr = localStorage.getItem("user");
  return userStr ? JSON.parse(userStr) : null;
}

/* Check token expiration and handle accordingly */
export async function checkTokenValidity() {
  if (!isAuthenticated()) {
    redirectToLogin();
    return false;
  }

  try {
    // Try to get user details to check if token is valid
    await API.get("user/details/");
    return true;
  } catch (error) {
    if (error.response?.status === 401) {
      // Token is invalid, clear storage and redirect to login
      console.log("Token validation failed, redirecting to login");
      localStorage.clear();
      redirectToLogin();
      return false;
    }
    // For other errors, let the calling code handle them
    throw error;
  }
}

/* Redirect to login page */
function redirectToLogin() {
  // Store current URL to redirect back after login
  const currentPath = window.location.pathname;
  if (currentPath !== "/login/" && currentPath !== "/register/" && currentPath !== "/logout/") {
    localStorage.setItem("redirectAfterLogin", currentPath);
  }
  window.location.href = "/login/";
}

/* Initialize authentication check on page load */
export function initAuth() {
  // Don't check auth on login/register pages to prevent redirect loops
  const currentPath = window.location.pathname;
  if (currentPath === "/login/" || currentPath === "/register/" || currentPath === "/logout/") {
    return;
  }
  
  // Check token validity when page loads
  checkTokenValidity().catch(error => {
    console.error("Auth initialization error:", error);
  });
}

/* ---------- helpers ---------- */
function persistUser({ access, refresh, user }) {
  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);
  localStorage.setItem("user", JSON.stringify(user));
  
  // Redirect to stored path or home
  const redirectPath = localStorage.getItem("redirectAfterLogin");
  if (redirectPath) {
    localStorage.removeItem("redirectAfterLogin");
    location.href = redirectPath;
  } else {
    location.href = "/";
  }
}
