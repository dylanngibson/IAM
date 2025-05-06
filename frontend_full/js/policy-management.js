import { api } from "./api.js";

console.log("✅ JS loaded for Policy Management page");

document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ DOM fully loaded");

  const form = document.querySelector(".policy-form");
  const deleteBtn = document.querySelector(".delete-btn");

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

    // 2) Map your form’s radio-group names → resource labels
    const resourceMap = {
      personal: "Personal Information",
      medical: "Medical Records",
      financial: "Financial Data",
      facility: "Facility Access",
      system: "System Configuration",
      audit: "Audit Logs",
    };

    // 3) Build the rules array from the selected radio buttons
    const rules = Object.keys(resourceMap).map((key) => {
      const sel = document.querySelector(`input[name="${key}"]:checked`);
      return {
        resource: resourceMap[key],
        access_level: (sel && convertToAccessLevel(sel.value)) || "no_access",
      };
    });

    function convertToAccessLevel(val) {
      if (val === "read") return "read_only";
      if (val === "write") return "read_write";
      if (val === "full") return "full_access";
      return "no_access";
    }

    const payload = {
      name,
      description,
      applies_to: appliesTo,
      rules,
    };

    try {
      const response = await api("/api/policies/", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      console.log("✅ Policy created:", response);
      alert("Policy created successfully!");

      // Optional: reload if you want to show it in the list immediately
      // location.reload();
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

    if (checked.length === 0) {
      alert("Please select at least one policy to delete.");
      return;
    }

    for (let cb of checked) {
      const policyId = cb.dataset.policyId;
      if (!policyId) {
        console.warn("Missing data-policy-id on checkbox:", cb);
        continue;
      }

      try {
        await api(`/api/policies/${policyId}/`, { method: "DELETE" });
        console.log(`✅ Deleted policy ID ${policyId}`);
      } catch (err) {
        console.error(`❌ Failed to delete policy ${policyId}:`, err);
      }
    }

    alert("Selected policies deleted.");
    location.reload();
  });
});
