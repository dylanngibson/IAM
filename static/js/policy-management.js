// static/js/policy-management.js
import { api } from "./api.js";

console.log("🛠️ Loaded UPDATED policy-management.js"); // <— you MUST see this in your console
console.log("✅ JS loaded for Policy Management page");

document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ DOM fully loaded");

  const form = document.querySelector(".policy-form");
  const deleteBtn = document.querySelector(".delete-btn");
  const listContainer = document.querySelector(".policy-list");

  // ——— CREATE POLICY ———
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("policyName").value.trim();
    const description = document
      .getElementById("policyDescription")
      .value.trim();
    if (!name) {
      alert("Policy name is required.");
      return;
    }

    // 1) Collect “Applies To” roles
    const appliesTo = Array.from(
      document.querySelectorAll(
        ".checkbox-group input[type='checkbox']:checked"
      )
    ).map((cb) => cb.parentElement.textContent.trim());

    // 2) Map radio-group names → resource labels
    const resourceMap = {
      personal: "Personal Information",
      medical: "Medical Records",
      financial: "Financial Data",
      facility: "Facility Access",
      system: "System Configuration",
      audit: "Audit Logs",
    };

    // 3) Build rules array
    const rules = Object.keys(resourceMap).map((key) => {
      const sel = document.querySelector(`input[name="${key}"]:checked`);
      return {
        resource: resourceMap[key],
        access_level:
          (sel &&
            { read: "read_only", write: "read_write", full: "full_access" }[
              sel.value
            ]) ||
          "no_access",
      };
    });

    const payload = { name, description, applies_to: appliesTo, rules };
    console.log("📤 PAYLOAD:", payload);

    try {
      // ▶️ POST to /api/roles/policies/
      const response = await api("roles/policies", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      console.log("✅ Policy created:", response);
      alert("Policy created successfully!");
      loadPolicies();
    } catch (err) {
      console.error("❌ Failed to create policy:", err);
      alert("Failed to create policy.");
    }
  });

  // ——— DELETE POLICY(IES) ———
  deleteBtn.addEventListener("click", async () => {
    const checked = Array.from(
      document.querySelectorAll(".policy-list input[type='checkbox']:checked")
    );
    if (!checked.length) {
      alert("Please select at least one policy to delete.");
      return;
    }

    for (let cb of checked) {
      const id = cb.dataset.policyId;
      try {
        // ▶️ DELETE at /api/roles/policies/{id}/
        await api(`roles/policies/${id}`, { method: "DELETE" });
        console.log(`✅ Deleted policy ID ${id}`);
      } catch (err) {
        console.error(`❌ Failed to delete policy ${id}:`, err);
      }
    }

    alert("Selected policies deleted.");
    loadPolicies();
  });

  // ——— FETCH & RENDER EXISTING POLICIES ———
  async function loadPolicies() {
    listContainer.innerHTML = "<p>Loading policies…</p>";
    try {
      // ▶️ GET from /api/roles/policies/
      const policies = await api("roles/policies");
      listContainer.innerHTML = "";
      policies.forEach((p) => {
        const item = document.createElement("div");
        item.className = "policy-item";
        item.innerHTML = `
          <input type="checkbox" data-policy-id="${p.id}" id="policy-${p.id}" />
          <label for="policy-${p.id}">${p.name}</label>
          <div class="policy-desc">${p.description || ""}</div>
        `;
        listContainer.appendChild(item);
      });
    } catch (err) {
      console.error("❌ Could not load policies:", err);
      listContainer.textContent = "Failed to load policies.";
    }
  }

  // Initial load
  loadPolicies();
});
