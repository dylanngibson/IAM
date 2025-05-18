// js/new-client.js
import { api } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".client-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const firstName = document.getElementById("firstName").value.trim();
    const lastName = document.getElementById("lastName").value.trim();
    const email = document.getElementById("email").value.trim();
    if (!firstName || !lastName || !email) {
      return alert("First name, last name, and email are required.");
    }
    const pwd = prompt("Set a password for the new client:");
    if (!pwd) return alert("Password is required.");
    await api("/api/users/create/", {
      method: "POST",
      body: JSON.stringify({
        username: `${firstName.toLowerCase()}.${lastName.toLowerCase()}`,
        email,
        password: pwd,
      }),
    });
    alert("Client created successfully.");
    form.reset();
  });
});
