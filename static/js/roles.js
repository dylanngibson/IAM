// js/roles.js
import { api } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  const listEl = document.querySelector(".role-list");
  const formEl = document.querySelector(".role-form");
  if (formEl) {
    formEl.addEventListener("submit", async (e) => {
      e.preventDefault();
      const name = document.getElementById("roleName").value.trim();
      if (!name) return alert("Role name required.");
      await api("/api/roles/", {
        method: "POST",
        body: JSON.stringify({ name }),
      });
      alert("Role created.");
      formEl.reset();
      loadRoles();
    });
  }
  async function loadRoles() {
    if (!listEl) return;
    const roles = await api("/api/roles/");
    listEl.innerHTML = roles
      .map(
        (r) => `
      <li data-id="${r.id}">
        ${r.name}
        <button class="del-role" data-id="${r.id}">×</button>
      </li>
    `
      )
      .join("");
    listEl.querySelectorAll(".del-role").forEach((b) =>
      b.addEventListener("click", async () => {
        if (!confirm("Delete this role?")) return;
        await api(`/api/roles/${b.dataset.id}/`, { method: "DELETE" });
        loadRoles();
      })
    );
  }
  loadRoles();
});
