// js/attributes.js
import { api } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  const listEl = document.querySelector(".attribute-list");
  const formEl = document.querySelector(".attribute-form");
  if (formEl) {
    formEl.addEventListener("submit", async (e) => {
      e.preventDefault();
      const key = document.getElementById("attrKey").value.trim();
      const val = document.getElementById("attrValue").value.trim();
      if (!key || !val) return alert("Key and value required.");
      await api("/api/attributes/", {
        method: "POST",
        body: JSON.stringify({ key, value: val }),
      });
      formEl.reset();
      loadAttrs();
    });
  }
  async function loadAttrs() {
    if (!listEl) return;
    const attrs = await api("/api/attributes/");
    listEl.innerHTML = attrs
      .map(
        (a) => `
      <li data-id="${a.id}">
        ${a.key}=${a.value}
        <button class="del-attr" data-id="${a.id}">×</button>
      </li>
    `
      )
      .join("");
    listEl.querySelectorAll(".del-attr").forEach((b) =>
      b.addEventListener("click", async () => {
        await api(`/api/attributes/${b.dataset.id}/`, { method: "DELETE" });
        loadAttrs();
      })
    );
  }
  loadAttrs();
});
