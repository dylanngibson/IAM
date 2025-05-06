// alerts.js - polling for new security alerts
import { api } from "./api.js";
let lastCheck = new Date().toISOString();
async function pollAlerts() {
  try {
    const alerts = await api("/alerts/?since=" + encodeURIComponent(lastCheck));
    alerts.forEach((a) => alert("ALERT: " + a.message));
    lastCheck = new Date().toISOString();
  } catch (e) {
    console.warn("Alert polling error", e);
  }
}
setInterval(pollAlerts, 5000);
pollAlerts();
