// js/exiting-client.js
import { api } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".exit-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const clientId = prompt("Enter client ID to deactivate:");
    if (!clientId) return alert("Client ID required.");
    if (!confirm("Are you sure you want to deactivate this client?")) return;
    // we’ll delete the user record to simulate deactivation
    await api(`/api/users/${clientId}/delete/`, { method: "DELETE" });
    alert("Client deactivated.");
    form.reset();
  });
});
