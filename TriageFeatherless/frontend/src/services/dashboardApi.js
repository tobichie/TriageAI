// Relative by default (nginx / Vite proxy handle routing to dashboard:8001).
// Override with VITE_DASHBOARD_API_URL only to bypass the proxy.
const DASHBOARD_API_URL =
    import.meta.env.VITE_DASHBOARD_API_URL || "/dashboard-api";

async function request(path, options) {
    const response = await fetch(`${DASHBOARD_API_URL}${path}`, options);

    if (!response.ok) {
        let detail = "";
        try {
            const body = await response.json();
            detail = body.detail || "";
        } catch {
            // ignore
        }
        throw new Error(detail || `Request failed (${response.status}).`);
    }

    return await response.json();
}

export function getPatients(includeDone = true) {
    return request(`/patients?include_done=${includeDone}`);
}

export function getPatient(patientId) {
    return request(`/patients/${patientId}`);
}

export function getStats() {
    return request(`/stats`);
}

export function updatePatient(patientId, patientData) {
    return request(`/patients/${patientId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(patientData),
    });
}

export function setPatientStatus(patientId, status) {
    return request(`/patients/${patientId}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
    });
}

export function deletePatient(patientId) {
    return request(`/patients/${patientId}`, { method: "DELETE" });
}
