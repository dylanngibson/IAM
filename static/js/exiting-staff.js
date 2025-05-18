// js/exiting-staff.js
import { api } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".staff-exit-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const staffId = prompt("Enter staff ID to deactivate:");
    if (!staffId) return alert("Staff ID required.");
    if (!confirm("Deactivate this staff member?")) return;
    await api(`/api/users/${staffId}/delete/`, { method: "DELETE" });
    alert("Staff deactivated.");
    form.reset();
  });
});
