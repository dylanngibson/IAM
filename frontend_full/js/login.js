// js/login.js
const API_ROOT = "http://127.0.0.1:8000";
console.log("🟢 login.js loaded");

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  console.log("→ submitting", { username, password });

  const res = await fetch(`${API_ROOT}/api-token-auth/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  console.log("← got response", res.status);
  const data = await res.json();

  if (!res.ok) {
    console.error("Login failed:", data);
    return alert(
      data.non_field_errors?.join(", ") || data.detail || "Login failed"
    );
  }

  localStorage.setItem("authToken", data.token);
  window.location.href = "/pages/index.html"; // or wherever your dashboard lives
});
