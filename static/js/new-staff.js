// js/new-staff.js
import { api } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".staff-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const firstName = form.querySelector("input[type='text']").value.trim();
    const email = form.querySelector("input[type='email']").value.trim();
    if (!firstName || !email) {
      return alert("Name and email are required.");
    }
    const pwd = prompt("Set a password for the new staff member:");
    if (!pwd) return alert("Password is required.");
    await api("/api/users/create/", {
      method: "POST",
      body: JSON.stringify({
        username: firstName.toLowerCase(),
        email,
        password: pwd,
      }),
    });
    alert("Staff member created.");
    form.reset();
  });
});
