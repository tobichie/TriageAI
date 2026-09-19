import { useEffect, useState } from "react";
import {
    getPatients,
    getStats,
    updatePatient,
    deletePatient,
} from "../services/dashboardApi";
import { priorityFor, STATUS_LABELS } from "../triage";

function stripe(prio) {
    return prio.className.replace("prio-", "");
}

function Records({ onReassess }) {
    const [patients, setPatients] = useState([]);
    const [stats, setStats] = useState(null);
    const [selected, setSelected] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [editing, setEditing] = useState(false);
    const [busy, setBusy] = useState(false);
    const [form, setForm] = useState({});

    async function load(keepId) {
        try {
            setLoading(true);
            setError(null);
            const [list, s] = await Promise.all([
                getPatients(true),
                getStats(),
            ]);
            setPatients(list);
            setStats(s);
            if (keepId != null) {
                const found = list.find((p) => p.id === keepId);
                setSelected(found || null);
            }
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        load();
    }, []);

    function select(patient) {
        setSelected(patient);
        setEditing(false);
    }

    function startEdit() {
        setForm({
            name: selected.name || "",
            age: selected.age != null ? String(selected.age) : "",
            clinical_context: selected.clinical_context || "",
        });
        setEditing(true);
    }

    async function saveEdit() {
        try {
            setBusy(true);
            setError(null);
            const changes = {
                name: form.name.trim() || null,
                age: form.age === "" ? null : Number(form.age),
                clinical_context: form.clinical_context.trim() || null,
            };
            const updated = await updatePatient(selected.id, changes);
            setSelected(updated);
            setEditing(false);
            await load(selected.id);
        } catch (e) {
            setError(e.message);
        } finally {
            setBusy(false);
        }
    }

    async function remove(patient) {
        if (
            !window.confirm(
                `Delete record for ${
                    patient.name || "Patient #" + patient.id
                }? This cannot be undone.`
            )
        ) {
            return;
        }
        try {
            setBusy(true);
            setError(null);
            await deletePatient(patient.id);
            setSelected(null);
            await load();
        } catch (e) {
            setError(e.message);
        } finally {
            setBusy(false);
        }
    }

    const vitals = selected?.vital_signs || {};

    return (
        <div className="page page-wide">
            <div className="page-head">
                <div>
                    <h2>Patient records</h2>
                    <p>View, correct and manage every triage encounter.</p>
                </div>
                <div className="head-actions">
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={() => load(selected?.id)}
                    >
                        ↻ Refresh
                    </button>
                </div>
            </div>

            {stats && (
                <div className="stat-tiles">
                    <div className="stat-tile accent">
                        <div className="k">Total encounters</div>
                        <div className="v">{stats.total}</div>
                    </div>
                    <div className="stat-tile">
                        <div className="k">Waiting</div>
                        <div className="v">{stats.waiting}</div>
                    </div>
                    <div className="stat-tile">
                        <div className="k">In treatment</div>
                        <div className="v">{stats.in_treatment}</div>
                    </div>
                    <div className="stat-tile">
                        <div className="k">Done</div>
                        <div className="v">{stats.done}</div>
                    </div>
                </div>
            )}

            {error && (
                <div className="error-banner">
                    <span>⚠</span>
                    <div>
                        <strong>Error</strong>
                        <p>{error}</p>
                    </div>
                </div>
            )}

            {loading ? (
                <div className="loading">
                    <span className="spinner" /> Loading records…
                </div>
            ) : (
                <div className="records-layout">
                    {/* LIST -------------------------------------- */}
                    <div className="card card-pad">
                        <div className="card-head">
                            <h2>All patients</h2>
                            <p>{patients.length} records</p>
                        </div>
                        {patients.length === 0 ? (
                            <p className="field-hint">No records yet.</p>
                        ) : (
                            <div className="rec-list">
                                {patients.map((p) => {
                                    const prio = priorityFor(
                                        p.triage_group
                                    );
                                    return (
                                        <button
                                            key={p.id}
                                            className={
                                                "rec-item" +
                                                (selected?.id === p.id
                                                    ? " selected"
                                                    : "")
                                            }
                                            onClick={() => select(p)}
                                        >
                                            <span
                                                className="rec-dot"
                                                style={{
                                                    background: prio.color,
                                                }}
                                            />
                                            <span className="r-body">
                                                <span className="r-name">
                                                    {p.name ||
                                                        `Patient #${p.id}`}
                                                </span>
                                                <span className="r-sub">
                                                    {p.age != null
                                                        ? `${p.age} yrs · `
                                                        : ""}
                                                    {STATUS_LABELS[
                                                        p.status
                                                    ] || p.status}
                                                </span>
                                            </span>
                                            <span className="r-grp">
                                                P{p.triage_group ?? "–"}
                                            </span>
                                        </button>
                                    );
                                })}
                            </div>
                        )}
                    </div>

                    {/* DETAIL ------------------------------------ */}
                    <div className="card card-pad">
                        {!selected ? (
                            <div className="empty">
                                <div className="empty-ico">◎</div>
                                <h2>Select a record</h2>
                                <p>
                                    Choose a patient from the list to view or
                                    edit their encounter.
                                </p>
                            </div>
                        ) : (
                            <>
                                <div className="detail-head">
                                    <div>
                                        <h3>
                                            {selected.name ||
                                                `Patient #${selected.id}`}
                                        </h3>
                                        <div className="d-sub">
                                            #{selected.id} ·{" "}
                                            <span
                                                className={`pill pill-${selected.status}`}
                                            >
                                                {STATUS_LABELS[
                                                    selected.status
                                                ] || selected.status}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="head-actions">
                                        {!editing && (
                                            <button
                                                className="btn btn-secondary btn-sm"
                                                onClick={startEdit}
                                            >
                                                Edit
                                            </button>
                                        )}
                                        <button
                                            className="btn btn-secondary btn-sm"
                                            onClick={() =>
                                                onReassess(selected)
                                            }
                                        >
                                            Re-assess
                                        </button>
                                        <button
                                            className="btn btn-danger btn-sm"
                                            disabled={busy}
                                            onClick={() => remove(selected)}
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </div>

                                {editing ? (
                                    <div className="detail-section">
                                        <h4>Edit details</h4>
                                        <div
                                            className="field-row"
                                            style={{ marginBottom: 14 }}
                                        >
                                            <div className="field">
                                                <label>Name</label>
                                                <input
                                                    value={form.name}
                                                    onChange={(e) =>
                                                        setForm({
                                                            ...form,
                                                            name: e.target
                                                                .value,
                                                        })
                                                    }
                                                />
                                            </div>
                                            <div className="field">
                                                <label>Age</label>
                                                <input
                                                    type="number"
                                                    value={form.age}
                                                    onChange={(e) =>
                                                        setForm({
                                                            ...form,
                                                            age: e.target
                                                                .value,
                                                        })
                                                    }
                                                />
                                            </div>
                                        </div>
                                        <div
                                            className="field"
                                            style={{ marginBottom: 14 }}
                                        >
                                            <label>Clinical context</label>
                                            <textarea
                                                rows="3"
                                                value={
                                                    form.clinical_context
                                                }
                                                onChange={(e) =>
                                                    setForm({
                                                        ...form,
                                                        clinical_context:
                                                            e.target.value,
                                                    })
                                                }
                                            />
                                        </div>
                                        <div className="head-actions">
                                            <button
                                                className="btn btn-primary btn-sm"
                                                disabled={busy}
                                                onClick={saveEdit}
                                            >
                                                Save changes
                                            </button>
                                            <button
                                                className="btn btn-ghost btn-sm"
                                                onClick={() =>
                                                    setEditing(false)
                                                }
                                            >
                                                Cancel
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    <>
                                        <div className="detail-section">
                                            <h4>Triage outcome</h4>
                                            <div className="kv-grid">
                                                <div className="kv">
                                                    <div className="k">
                                                        Priority
                                                    </div>
                                                    <div className="v">
                                                        {selected.triage_group ??
                                                            "—"}{" "}
                                                        <span
                                                            style={{
                                                                fontSize: 13,
                                                                color: "var(--text-3)",
                                                            }}
                                                        >
                                                            {selected.treatment_priority ||
                                                                ""}
                                                        </span>
                                                    </div>
                                                </div>
                                                <div className="kv">
                                                    <div className="k">
                                                        AI priority
                                                    </div>
                                                    <div className="v">
                                                        {selected.ai_severity ??
                                                            "—"}
                                                    </div>
                                                </div>
                                                <div className="kv">
                                                    <div className="k">
                                                        Target wait
                                                    </div>
                                                    <div className="v">
                                                        {selected.max_wait_minutes !=
                                                        null
                                                            ? `${selected.max_wait_minutes}m`
                                                            : "—"}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="detail-section">
                                            <h4>Symptoms</h4>
                                            {selected.symptoms?.length ? (
                                                <div className="sym-list">
                                                    {selected.symptoms.map(
                                                        (s, i) => (
                                                            <div
                                                                className="sym-item"
                                                                key={i}
                                                            >
                                                                <span className="s-name">
                                                                    {s.name}
                                                                </span>
                                                                <span className="s-meta">
                                                                    {s.severity !=
                                                                        null && (
                                                                        <span>
                                                                            {
                                                                                s.severity
                                                                            }
                                                                            /10
                                                                        </span>
                                                                    )}
                                                                    {s.duration_minutes !=
                                                                        null && (
                                                                        <span>
                                                                            {
                                                                                s.duration_minutes
                                                                            }
                                                                            {" "}
                                                                            min
                                                                        </span>
                                                                    )}
                                                                </span>
                                                            </div>
                                                        )
                                                    )}
                                                </div>
                                            ) : (
                                                <p className="field-hint">
                                                    No symptoms recorded.
                                                </p>
                                            )}
                                        </div>

                                        <div className="detail-section">
                                            <h4>Vital signs</h4>
                                            <div className="kv-grid">
                                                <div className="kv">
                                                    <div className="k">
                                                        Heart rate
                                                    </div>
                                                    <div className="v">
                                                        {vitals.heart_rate ??
                                                            "—"}
                                                    </div>
                                                </div>
                                                <div className="kv">
                                                    <div className="k">
                                                        Blood pressure
                                                    </div>
                                                    <div className="v">
                                                        {vitals.systolic_bp ??
                                                            "—"}
                                                        /
                                                        {vitals.diastolic_bp ??
                                                            "—"}
                                                    </div>
                                                </div>
                                                <div className="kv">
                                                    <div className="k">
                                                        SpO₂
                                                    </div>
                                                    <div className="v">
                                                        {vitals.oxygen_saturation ??
                                                            "—"}
                                                        %
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="detail-section">
                                            <h4>Clinical context</h4>
                                            <p
                                                style={{
                                                    fontSize: 14,
                                                    lineHeight: 1.6,
                                                    color: "var(--text)",
                                                }}
                                            >
                                                {selected.clinical_context ||
                                                    "No clinical context provided."}
                                            </p>
                                        </div>

                                        {selected.ai_reason && (
                                            <div className="detail-section">
                                                <h4>AI reasoning</h4>
                                                <p
                                                    style={{
                                                        fontSize: 14,
                                                        lineHeight: 1.6,
                                                    }}
                                                >
                                                    {selected.ai_reason}
                                                </p>
                                            </div>
                                        )}
                                    </>
                                )}
                            </>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

export default Records;
