// api.js - basic fetch wrapper for Django backend
const API_ROOT = "http://127.0.0.1:8000";
export async function api(path, opts = {}) {
    const token = localStorage.getItem("authToken");
    const headers = { "Content-Type": "application/json", ...opts.headers };
    if (token) headers["Authorization"] = `Token ${token}`;
    const res = await fetch(API_ROOT + path, { ...opts, headers });
    if (res.status === 401) window.location = "login.html";
    return res.ok ? res.json() : Promise.reject(await res.json());
}