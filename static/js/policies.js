// js/policies.js
import { api } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  const section = document.querySelector(".policy-section");
  const roleId = section.dataset.roleId;

  // Buttons
  const createBtn = document.getElementById("create-policy-btn");
  const deleteBtn = document.getElementById("delete-policy-btn");

  // Helper: get all checked policy names
  function getCheckedPolicies() {
    return Array.from(
      section.querySelectorAll(".policy-list input:checked")
    ).map((cb) => cb.parentElement.textContent.trim());
  }

  // 🔹 Create new role (policy)
  document
    .getElementById("new-policy-btn")
    .addEventListener("click", async () => {
      const name = prompt("Enter new policy (role) name:");
      if (!name) return;

      try {
        const response = await api("/roles/roles/", {
          method: "POST",
          body: JSON.stringify({ name }),
        });

        alert("New policy created!");
        location.reload();
      } catch (err) {
        console.error(err);
        alert("Failed to create policy.");
      }
    });

  // 🔸 Assign permissions
  createBtn.addEventListener("click", async () => {
    const perms = getCheckedPolicies();
    try {
      await api(`/roles/${roleId}/set_permissions/`, {
        method: "POST",
        body: JSON.stringify({ permissions: perms }),
      });
      alert("Policies updated successfully!");
    } catch (err) {
      console.error(err);
      alert("Failed to update policies.");
    }
  });

  // 🔻 Remove permissions
  deleteBtn.addEventListener("click", async () => {
    const perms = getCheckedPolicies();
    try {
      await api(`/roles/${roleId}/remove_permissions/`, {
        method: "POST",
        body: JSON.stringify({ permissions: perms }),
      });
      alert("Policies removed successfully!");
    } catch (err) {
      console.error(err);
      alert("Failed to remove policies.");
    }
  });
});
