const API_ROOT = "http://127.0.0.1:8000";
console.log("🟢 login.js loaded");

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");

  // Create or get error message element
  let errorMessage = document.getElementById("login-error");
  if (!errorMessage) {
    errorMessage = document.createElement("div");
    errorMessage.id = "login-error";
    errorMessage.style.color = "red";
    errorMessage.style.marginTop = "10px";
    errorMessage.style.textAlign = "center";
    form.appendChild(errorMessage);
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    console.log("→ submitting", { username, password });

    const res = await fetch(`${API_ROOT}/api-token-auth/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    let data;
    try {
      data = await res.json();
    } catch (err) {
      errorMessage.textContent = "Unexpected server error.";
      return;
    }

    if (!res.ok) {
      console.error("Login failed:", data);

      // Show inline error instead of alert popup
      errorMessage.textContent =
        data.non_field_errors?.join(", ") || data.detail || "Login failed";

      // Clear form fields
      document.getElementById("username").value = "";
      document.getElementById("password").value = "";

      return;
    }

    // ✅ Successful login
    localStorage.setItem("authToken", data.token);
    window.location.href = "/pages/index.html";
  });
});
