// Base URL for the main API.
//
// Default is the RELATIVE path "/api", which is the smart, portable option:
// - Behind the domain, nginx proxies /api -> backend:8000.
// - On the Vite dev server directly, vite.config.js proxies /api -> backend.
// Same origin means no CORS and Basic-Auth credentials are sent automatically.
//
// Override with an absolute URL (e.g. http://<host-ip>:8000) via
// VITE_API_URL only if you ever want to bypass the proxy.
const API_URL = import.meta.env.VITE_API_URL || "/api";

// Returns true when GET /api/health responds with {status: "healthy"}.
// Throws / returns false when the backend is unreachable or unhealthy.
export async function checkHealth() {
    const response = await fetch(`${API_URL}/health`, { method: "GET" });

    if (!response.ok) {
        return false;
    }

    const data = await response.json();
    return data.status === "healthy";
}

export async function assessPatient(patientData) {
    const response = await fetch(`${API_URL}/triage`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(patientData),
    });

    if (!response.ok) {
        throw new Error("Failed to assess patient.");
    }

    return await response.json();
}
