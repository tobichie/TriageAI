import { useState } from "react";
import { priorityFor } from "../triage";

function cleanExplanation(text) {
    return (text || "")
        .replace(/## /g, "")
        .replace(/\*\*/g, "")
        .replace(/^- /gm, "• ");
}

function AssessmentResult({ data }) {
    const [showExplanation, setShowExplanation] = useState(false);

    if (!data) {
        return null;
    }

    const result = data.triage_result;
    const ai = data.ai_assessment;
    const prio = priorityFor(result.suggested_group);
    const aiPrio = priorityFor(ai?.severity);

    const matches =
        ai && Number(result.suggested_group) === Number(ai.severity);

    const redFlags = result.red_flags || [];
    const factors = result.relevant_factors || [];

    const explanationParas = cleanExplanation(data.ai_explanation)
        .split("\n\n")
        .map((p) => p.trim())
        .filter(Boolean);

    return (
        <div className="result-scroll">
            {/* PRIORITY BANNER ----------------------------------- */}
            <div className={`result-banner ${prio.className}`}>
                <div className="group-badge">{result.suggested_group}</div>
                <div className="banner-body">
                    <div className="short">
                        Priority {result.suggested_group} · {prio.short}
                    </div>
                    <h2>{result.treatment_priority}</h2>
                    <p>
                        {data.patient_id
                            ? "Saved to the triage board. "
                            : ""}
                        {result.protocol_name} {result.protocol_version}
                    </p>
                </div>
            </div>

            {/* META ---------------------------------------------- */}
            <div className="meta-row">
                <div className="meta-tile">
                    <div className="label">Target wait</div>
                    <div className="value">
                        {result.max_wait_minutes}
                        <small> min</small>
                    </div>
                </div>
                <div className="meta-tile">
                    <div className="label">Re-evaluate</div>
                    <div className="value">
                        {result.reevaluation_minutes != null
                            ? result.reevaluation_minutes
                            : "—"}
                        <small>
                            {result.reevaluation_minutes != null
                                ? " min"
                                : ""}
                        </small>
                    </div>
                </div>
                <div className="meta-tile">
                    <div className="label">Human review</div>
                    <div className="value">
                        {result.requires_human_review ? "Required" : "—"}
                    </div>
                </div>
            </div>

            {/* RED FLAGS ----------------------------------------- */}
            {redFlags.length > 0 && (
                <div className="card card-pad result-block redflag-block">
                    <h3>⚠ Red flags</h3>
                    <div className="factor-list">
                        {redFlags.map((flag, i) => (
                            <div className="redflag" key={i}>
                                <span>⚠</span>
                                {flag}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* WHY THIS PRIORITY (explainability) ---------------- */}
            <div className="card card-pad result-block">
                <h3>Why this priority</h3>
                {factors.length > 0 ? (
                    <div className="factor-list">
                        {factors.map((factor, i) => (
                            <div className="factor" key={i}>
                                <span className="dot" />
                                {factor}
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="field-hint">
                        No specific rules triggered. Priority defaults to the
                        least urgent group — confirm clinically.
                    </p>
                )}

                {result.missing_information?.length > 0 && (
                    <p className="field-hint" style={{ marginTop: 12 }}>
                        Missing data considered:{" "}
                        {result.missing_information.join(", ")}
                    </p>
                )}
            </div>

            {/* AI SECOND OPINION --------------------------------- */}
            {ai && (
                <div className="card card-pad result-block ai-card">
                    <div className="ai-head">
                        <div className="ai-badge">✦</div>
                        <div>
                            <h3>AI second opinion</h3>
                            <p>Independent — does not override the engine</p>
                        </div>
                        <span
                            className={`prio-tag tag-${aiPrio.className.replace(
                                "prio-",
                                ""
                            )}`}
                            style={{ marginLeft: "auto" }}
                        >
                            Priority {ai.severity}
                        </span>
                    </div>
                    <p className="ai-reason">{ai.reason}</p>

                    <div
                        className={`agreement ${
                            matches ? "match" : "mismatch"
                        }`}
                        style={{ marginTop: 16 }}
                    >
                        <div className="a-icon">{matches ? "✓" : "!"}</div>
                        <div>
                            <strong>
                                {matches
                                    ? "AI agrees with the engine"
                                    : "AI disagrees — review advised"}
                            </strong>
                            {!matches && (
                                <span>
                                    Engine: {result.suggested_group} · AI:{" "}
                                    {ai.severity}. Use clinical judgement.
                                </span>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* AI EXPLANATION ------------------------------------ */}
            {explanationParas.length > 0 && (
                <div className="card card-pad result-block">
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            marginBottom: showExplanation ? 14 : 0,
                        }}
                    >
                        <h3 style={{ marginBottom: 0 }}>
                            Detailed explanation
                        </h3>
                        <button
                            type="button"
                            className="btn btn-ghost btn-sm"
                            onClick={() =>
                                setShowExplanation((v) => !v)
                            }
                        >
                            {showExplanation ? "Hide" : "Show"}
                        </button>
                    </div>
                    {showExplanation && (
                        <div className="explanation-content">
                            {explanationParas.map((p, i) => (
                                <p key={i}>{p}</p>
                            ))}
                        </div>
                    )}
                </div>
            )}

            <p className="disclaimer">
                TriageAI is a clinical decision-support prototype, not a
                medical device. It does not diagnose and does not replace a
                qualified clinician. Every result requires human review.
            </p>
        </div>
    );
}

export default AssessmentResult;
