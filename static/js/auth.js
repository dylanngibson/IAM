// js/auth.js
import { api } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value.trim();
      const errEl = document.getElementById("login-error");
      errEl.textContent = "";

      try {
        // Step 1: username/password
        const data1 = await api("/auth/login/", {
          method: "POST",
          body: JSON.stringify({ username, password }),
        });

        // If MFA is required, prompt for OTP
        if (data1.mfa_required) {
          const otp = prompt("Enter OTP from your authenticator:");
          if (!otp) throw new Error("OTP required");

          const data2 = await api("/auth/mfa/verify/", {
            method: "POST",
            body: JSON.stringify({ mfa_token: data1.mfa_token, otp }),
          });

          // Save tokens and redirect
          localStorage.setItem("accessToken", data2.access);
          localStorage.setItem("refreshToken", data2.refresh);
          window.location.href = "index.html";
          return;
        }

        // No MFA: save tokens and redirect
        localStorage.setItem("accessToken", data1.access);
        localStorage.setItem("refreshToken", data1.refresh);
        window.location.href = "index.html";
      } catch (err) {
        console.error(err);
        errEl.textContent = err.message;
      }
    });
  }

  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      const refresh = localStorage.getItem("refreshToken");
      try {
        await api("/auth/logout/", {
          method: "POST",
          body: JSON.stringify({ refresh }),
        });
      } catch {
        // ignore errors on logout
      } finally {
        localStorage.clear();
        window.location.href = "login.html";
      }
    });
  }
});
