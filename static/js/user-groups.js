// js/user-groups.js
import { api } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  const panel = document.querySelector(".user-panel");
  if (!panel) return;

  async function loadUsers() {
    const users = await api("/api/users/");
    panel.innerHTML = users
      .map(
        (u) => `
        <div class="user-card">
          <div class="user-icon">${u.username.charAt(0).toUpperCase()}</div>
          <div class="user-info">
            <strong>${u.username}</strong><br/>
            ${u.email}
          </div>
          <div class="user-actions">
            <button class="delete-user-btn" data-id="${u.id}">Delete</button>
          </div>
        </div>
      `
      )
      .join("");
    panel.querySelectorAll(".delete-user-btn").forEach((btn) =>
      btn.addEventListener("click", async () => {
        if (!confirm("Delete this user?")) return;
        await api(`/api/users/${btn.dataset.id}/delete/`, { method: "DELETE" });
        loadUsers();
      })
    );
  }

  loadUsers();
});
