// static/js/api.js

// No trailing slash here:
const API_ROOT = "http://127.0.0.1:8000/api";

export async function api(path, opts = {}) {
  // 1) Remove any leading/trailing slashes
  let cleaned = path.replace(/^\/+|\/+$/g, "");
  // 2) If it still starts with "api/", strip that too:
  cleaned = cleaned.replace(/^api\//, "");
  // 3) Build URL with exactly one "/api/" prefix and trailing slash
  const url = `${API_ROOT}/${cleaned}/`;

  console.log("🛰️ FETCHING →", url, opts);

  const token = localStorage.getItem("accessToken");
  const headers = {
    "Content-Type": "application/json",
    ...(opts.headers || {}),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(url, { ...opts, headers });

  if (!res.ok) {
    // Log out the raw backend response for debugging
    const text = await res.text();
    console.error(`🚨 ${res.status} RESPONSE BODY:\n`, text);
    throw new Error(`Request failed ${res.status}`);
  }

  return res.json();
}
