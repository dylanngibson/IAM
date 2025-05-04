import { api } from "./api.js";

console.log("✅ JS loaded for Policy Management page");

document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ DOM fully loaded");

  const createBtn = document.querySelector(".submit-btn");
  const deleteBtn = document.querySelector(".delete-btn");

  // CREATE POLICY
  createBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const name = document.getElementById("policyName").value.trim();
    const description = document
      .getElementById("policyDescription")
      .value.trim();

    if (!name) {
      alert("Policy name is required.");
      return;
    }

    try {
      const response = await api("/roles/roles/", {
        method: "POST",
        body: JSON.stringify({ name, description }),
      });
      console.log("✅ Policy created:", response);
      alert("Policy created!");
      location.reload();
    } catch (err) {
      console.error("❌ Failed to create policy:", err);
      alert("Failed to create policy.");
    }
  });

  // DELETE POLICY
  deleteBtn.addEventListener("click", async () => {
    const checked = Array.from(
      document.querySelectorAll(".policy-list input:checked")
    );
    if (checked.length === 0) {
      alert("Please select at least one policy to delete.");
      return;
    }

    for (let cb of checked) {
      const policyName = cb.nextElementSibling.textContent.trim();
      try {
        await api(`/roles/roles/${policyName}/`, {
          method: "DELETE",
        });
        console.log(`✅ Deleted ${policyName}`);
      } catch (err) {
        console.error(`❌ Failed to delete ${policyName}:`, err);
      }
    }

    alert("Selected policies deleted.");
    location.reload();
  });
});
