// Shared triage display helpers.
//
// The backend uses the Manchester-style 5-level scheme
// (group 1 = most urgent ... group 5 = least urgent) and returns a
// colour name. This module maps that to consistent UI metadata so the
// intake result, the board and the records view all look the same.

export const PRIORITY = {
    1: {
        group: 1,
        label: "Immediate",
        short: "SOFORT",
        className: "prio-red",
        color: "#dc2626",
    },
    2: {
        group: 2,
        label: "Very Urgent",
        short: "SEHR DRINGEND",
        className: "prio-orange",
        color: "#ea580c",
    },
    3: {
        group: 3,
        label: "Urgent",
        short: "DRINGEND",
        className: "prio-yellow",
        color: "#d97706",
    },
    4: {
        group: 4,
        label: "Normal",
        short: "NORMAL",
        className: "prio-green",
        color: "#16a34a",
    },
    5: {
        group: 5,
        label: "Not Urgent",
        short: "NICHT DRINGEND",
        className: "prio-blue",
        color: "#2563eb",
    },
};

export const UNKNOWN_PRIORITY = {
    group: null,
    label: "Not assessed",
    short: "—",
    className: "prio-none",
    color: "#94a3b8",
};

export function priorityFor(group) {
    return PRIORITY[group] || UNKNOWN_PRIORITY;
}

export const STATUS_LABELS = {
    waiting: "Waiting",
    in_treatment: "In treatment",
    done: "Done",
};

// Minutes elapsed since an ISO timestamp.
export function minutesSince(isoString) {
    if (!isoString) {
        return null;
    }

    const then = new Date(isoString).getTime();

    if (Number.isNaN(then)) {
        return null;
    }

    return Math.max(0, Math.floor((Date.now() - then) / 60000));
}

export function formatWaited(minutes) {
    if (minutes == null) {
        return "—";
    }

    if (minutes < 60) {
        return `${minutes} min`;
    }

    const hours = Math.floor(minutes / 60);
    const rest = minutes % 60;

    return `${hours} h ${rest} min`;
}

// True when the patient has waited longer than their target window.
export function isOverdue(patient) {
    if (patient.status === "done") {
        return false;
    }

    const waited = minutesSince(patient.created_at);

    if (waited == null || patient.max_wait_minutes == null) {
        return false;
    }

    return waited > patient.max_wait_minutes;
}
