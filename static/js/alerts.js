// js/alerts.js
import { api } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  const listEl = document.querySelector(".alert-list");
  const badgeEl = document.querySelector(".alert-badge");

  async function refreshAlerts() {
    const alerts = await api("/api/alerts/recent/");
    if (listEl) {
      listEl.innerHTML = alerts
        .map(
          (a) => `
        <div class="alert-item ${a.seen ? "seen" : "unseen"}">
          <div><strong>${a.level}</strong> @ ${new Date(
            a.timestamp
          ).toLocaleTimeString()}</div>
          <div>${a.message}</div>
          <button class="ack" data-id="${a.id}">Acknowledge</button>
        </div>
      `
        )
        .join("");
      listEl.querySelectorAll(".ack").forEach((b) =>
        b.addEventListener("click", async () => {
          await api(`/api/alerts/${b.dataset.id}/ack/`, { method: "POST" });
          refreshAlerts();
          refreshBadge();
        })
      );
    }
  }

  async function refreshBadge() {
    const { unseen_count } = await api("/api/alerts/unseen-count/");
    if (badgeEl) badgeEl.textContent = unseen_count;
  }

  refreshAlerts();
  refreshBadge();
  setInterval(refreshAlerts, 60000);
});
