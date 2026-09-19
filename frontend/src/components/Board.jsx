import { useEffect, useState } from "react";
import {
    getPatients,
    setPatientStatus,
} from "../services/dashboardApi";
import {
    priorityFor,
    minutesSince,
    formatWaited,
    isOverdue,
} from "../triage";

const FILTERS = [
    { key: "active", label: "Active" },
    { key: "all", label: "All" },
    { key: "done", label: "Done" },
];

const LEGEND = [1, 2, 3, 4, 5];

function stripeName(prio) {
    return prio.className.replace("prio-", "");
}

function Board({ onReassess }) {
    const [patients, setPatients] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState("active");
    const [busyId, setBusyId] = useState(null);
    // Tick to refresh the live wait timers.
    const [, setTick] = useState(0);

    async function load(quiet = false) {
        try {
            if (!quiet) setLoading(true);
            setError(null);
            const data = await getPatients(true);
            setPatients(data);
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        load();
        const reload = setInterval(() => load(true), 20000);
        const tick = setInterval(() => setTick((t) => t + 1), 30000);
        return () => {
            clearInterval(reload);
            clearInterval(tick);
        };
    }, []);

    async function changeStatus(patient, status) {
        try {
            setBusyId(patient.id);
            await setPatientStatus(patient.id, status);
            await load(true);
        } catch (e) {
            setError(e.message);
        } finally {
            setBusyId(null);
        }
    }

    const visible = patients.filter((p) => {
        if (filter === "all") return true;
        if (filter === "done") return p.status === "done";
        return p.status !== "done";
    });

    const waitingCount = patients.filter(
        (p) => p.status !== "done"
    ).length;
    const overdueCount = patients.filter(isOverdue).length;

    return (
        <div className="page page-wide">
            <div className="page-head">
                <div>
                    <h2>Triage board</h2>
                    <p>
                        {waitingCount} patient
                        {waitingCount === 1 ? "" : "s"} in the department
                        {overdueCount > 0 && (
                            <>
                                {" · "}
                                <strong style={{ color: "var(--danger)" }}>
                                    {overdueCount} overdue
                                </strong>
                            </>
                        )}
                    </p>
                </div>
                <div className="head-actions">
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={() => load()}
                    >
                        ↻ Refresh
                    </button>
                </div>
            </div>

            <div className="board-toolbar">
                <div className="seg">
                    {FILTERS.map((f) => (
                        <button
                            key={f.key}
                            className={filter === f.key ? "active" : ""}
                            onClick={() => setFilter(f.key)}
                        >
                            {f.label}
                        </button>
                    ))}
                </div>
                <div className="legend">
                    {LEGEND.map((g) => {
                        const p = priorityFor(g);
                        return (
                            <span key={g}>
                                <span
                                    className="swatch"
                                    style={{ background: p.color }}
                                />
                                {g} {p.label}
                            </span>
                        );
                    })}
                </div>
            </div>

            {error && (
                <div className="error-banner">
                    <span>⚠</span>
                    <div>
                        <strong>Could not load the board</strong>
                        <p>{error}</p>
                    </div>
                </div>
            )}

            {loading ? (
                <div className="loading">
                    <span className="spinner" /> Loading board…
                </div>
            ) : visible.length === 0 ? (
                <div className="card">
                    <div className="empty">
                        <div className="empty-ico">✓</div>
                        <h2>Nothing here</h2>
                        <p>
                            No patients match this filter. Assess a patient to
                            add them to the board.
                        </p>
                    </div>
                </div>
            ) : (
                <div className="board-grid">
                    {visible.map((patient) => {
                        const prio = priorityFor(patient.triage_group);
                        const stripe = stripeName(prio);
                        const waited = minutesSince(patient.created_at);
                        const overdue = isOverdue(patient);
                        const busy = busyId === patient.id;

                        return (
                            <div
                                key={patient.id}
                                className={
                                    `pcard stripe-${stripe}` +
                                    (overdue ? " overdue" : "") +
                                    (patient.status === "done"
                                        ? " done"
                                        : "")
                                }
                            >
                                <div className="pcard-top">
                                    <div className={`prio-badge badge-${stripe}`}>
                                        {patient.triage_group ?? "–"}
                                    </div>
                                    <div className="pcard-id">
                                        <div className="pname">
                                            {patient.name ||
                                                `Patient #${patient.id}`}
                                        </div>
                                        <div className="pmeta">
                                            {patient.age != null
                                                ? `${patient.age} yrs · `
                                                : ""}
                                            #{patient.id}
                                        </div>
                                        {patient.requires_human_review && (
                                            <span className="review-flag">
                                                ⚑ Human review
                                            </span>
                                        )}
                                    </div>
                                    <span className={`prio-tag tag-${stripe}`}>
                                        {prio.short}
                                    </span>
                                </div>

                                <div className="pcard-complaint">
                                    {patient.symptoms?.length ? (
                                        patient.symptoms
                                            .slice(0, 4)
                                            .map((s, i) => (
                                                <span
                                                    className="mini-chip"
                                                    key={i}
                                                >
                                                    {s.name}
                                                    {s.severity != null
                                                        ? ` ${s.severity}/10`
                                                        : ""}
                                                </span>
                                            ))
                                    ) : (
                                        <span className="mini-chip">
                                            No symptoms recorded
                                        </span>
                                    )}
                                </div>

                                <div className="pcard-wait">
                                    <div className="w-item">
                                        <span className="k">Waiting</span>
                                        <span className="v">
                                            {formatWaited(waited)}
                                        </span>
                                    </div>
                                    <div className="w-sep" />
                                    <div className="w-item">
                                        <span className="k">Target</span>
                                        <span className="v">
                                            {patient.max_wait_minutes != null
                                                ? `${patient.max_wait_minutes} min`
                                                : "—"}
                                        </span>
                                    </div>
                                    {overdue && (
                                        <span className="overdue-flag">
                                            Overdue
                                        </span>
                                    )}
                                    {!overdue &&
                                        patient.status !== "done" && (
                                            <span
                                                className={`pill pill-${patient.status}`}
                                                style={{
                                                    marginLeft: "auto",
                                                }}
                                            >
                                                {patient.status ===
                                                "in_treatment"
                                                    ? "In treatment"
                                                    : "Waiting"}
                                            </span>
                                        )}
                                    {patient.status === "done" && (
                                        <span
                                            className="pill pill-done"
                                            style={{ marginLeft: "auto" }}
                                        >
                                            Done
                                        </span>
                                    )}
                                </div>

                                <div className="pcard-actions">
                                    {patient.status === "waiting" && (
                                        <button
                                            className="btn btn-primary btn-sm"
                                            disabled={busy}
                                            onClick={() =>
                                                changeStatus(
                                                    patient,
                                                    "in_treatment"
                                                )
                                            }
                                        >
                                            Start treatment
                                        </button>
                                    )}
                                    {patient.status === "in_treatment" && (
                                        <button
                                            className="btn btn-primary btn-sm"
                                            disabled={busy}
                                            onClick={() =>
                                                changeStatus(
                                                    patient,
                                                    "done"
                                                )
                                            }
                                        >
                                            Mark done
                                        </button>
                                    )}
                                    {patient.status === "done" && (
                                        <button
                                            className="btn btn-secondary btn-sm"
                                            disabled={busy}
                                            onClick={() =>
                                                changeStatus(
                                                    patient,
                                                    "waiting"
                                                )
                                            }
                                        >
                                            Reopen
                                        </button>
                                    )}
                                    <button
                                        className="btn btn-ghost btn-sm"
                                        disabled={busy}
                                        onClick={() => onReassess(patient)}
                                    >
                                        Re-assess
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}

export default Board;
