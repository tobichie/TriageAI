import { useState } from "react";

const COMMON_COMPLAINTS = [
    "Chest pain",
    "Shortness of breath",
    "Abdominal pain",
    "Headache",
    "Fever",
    "Dizziness",
    "Bleeding",
    "Injury / trauma",
    "Fall",
    "Vomiting",
    "Back pain",
    "Unconscious",
];

const SEVERITY_LABELS = [
    "None",
    "Minimal",
    "Mild",
    "Mild",
    "Moderate",
    "Moderate",
    "Strong",
    "Strong",
    "Severe",
    "Severe",
    "Worst",
];

function emptySymptom() {
    return { name: "", severity: 5, duration_minutes: "" };
}

function initialSymptoms(initialData) {
    if (initialData?.symptoms?.length) {
        return initialData.symptoms.map((s) => ({
            name: s.name || "",
            severity: s.severity == null ? 5 : s.severity,
            duration_minutes:
                s.duration_minutes == null ? "" : s.duration_minutes,
        }));
    }
    return [emptySymptom()];
}

function PatientForm({ onSubmit, initialData }) {
    const vitals = initialData?.vital_signs || {};

    const [name, setName] = useState(initialData?.name || "");
    const [age, setAge] = useState(
        initialData?.age != null ? String(initialData.age) : ""
    );
    const [clinicalContext, setClinicalContext] = useState(
        initialData?.clinical_context || ""
    );
    const [heartRate, setHeartRate] = useState(
        vitals.heart_rate != null ? String(vitals.heart_rate) : ""
    );
    const [oxygenSaturation, setOxygenSaturation] = useState(
        vitals.oxygen_saturation != null
            ? String(vitals.oxygen_saturation)
            : ""
    );
    const [systolicBp, setSystolicBp] = useState(
        vitals.systolic_bp != null ? String(vitals.systolic_bp) : ""
    );
    const [diastolicBp, setDiastolicBp] = useState(
        vitals.diastolic_bp != null ? String(vitals.diastolic_bp) : ""
    );
    const [symptoms, setSymptoms] = useState(() =>
        initialSymptoms(initialData)
    );

    function updateSymptom(index, field, value) {
        setSymptoms((prev) => {
            const next = [...prev];
            next[index] = { ...next[index], [field]: value };
            return next;
        });
    }

    function addSymptom(prefillName = "") {
        setSymptoms((prev) => {
            // Reuse a trailing empty row if present.
            if (prev.length && prev[prev.length - 1].name.trim() === "") {
                const next = [...prev];
                next[next.length - 1] = {
                    ...next[next.length - 1],
                    name: prefillName,
                };
                return next;
            }
            return [...prev, { ...emptySymptom(), name: prefillName }];
        });
    }

    function removeSymptom(index) {
        setSymptoms((prev) =>
            prev.length === 1
                ? [emptySymptom()]
                : prev.filter((_, i) => i !== index)
        );
    }

    const selectedNames = new Set(
        symptoms.map((s) => s.name.trim().toLowerCase())
    );

    function toNum(value) {
        return value === "" || value == null ? null : Number(value);
    }

    function handleSubmit(event) {
        event.preventDefault();

        const cleanedSymptoms = symptoms
            .filter((s) => s.name.trim() !== "")
            .map((s) => ({
                name: s.name.trim(),
                severity: toNum(s.severity),
                duration_minutes: toNum(s.duration_minutes),
            }));

        onSubmit({
            name: name.trim() || null,
            age: toNum(age),
            symptoms: cleanedSymptoms,
            vital_signs: {
                heart_rate: toNum(heartRate),
                oxygen_saturation: toNum(oxygenSaturation),
                systolic_bp: toNum(systolicBp),
                diastolic_bp: toNum(diastolicBp),
            },
            clinical_context: clinicalContext.trim() || null,
        });
    }

    return (
        <form className="card card-pad" onSubmit={handleSubmit}>
            <div className="card-head">
                <h2>New patient intake</h2>
                <p>Capture what you see. Every field is optional — assess with what you have.</p>
            </div>

            {/* PATIENT ------------------------------------------------ */}
            <div className="form-section">
                <div className="section-label">
                    <span className="num">1</span> Patient
                </div>
                <div className="field-row">
                    <div className="field">
                        <label>Name / identifier</label>
                        <input
                            type="text"
                            placeholder="e.g. Anna Becker or Bed 4"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>
                    <div className="field">
                        <label>Age</label>
                        <div className="input-suffix">
                            <input
                                type="number"
                                placeholder="Years"
                                min="0"
                                max="130"
                                value={age}
                                onChange={(e) => setAge(e.target.value)}
                            />
                            <span>yrs</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* SYMPTOMS ----------------------------------------------- */}
            <div className="form-section">
                <div className="section-label">
                    <span className="num">2</span> Presenting complaint
                </div>

                <div className="field" style={{ marginBottom: 16 }}>
                    <span className="field-label">Quick add</span>
                    <div className="chips">
                        {COMMON_COMPLAINTS.map((complaint) => (
                            <button
                                key={complaint}
                                type="button"
                                className={
                                    "chip" +
                                    (selectedNames.has(
                                        complaint.toLowerCase()
                                    )
                                        ? " selected"
                                        : "")
                                }
                                onClick={() => addSymptom(complaint)}
                            >
                                {complaint}
                            </button>
                        ))}
                    </div>
                </div>

                {symptoms.map((symptom, index) => (
                    <div className="symptom-card" key={index}>
                        <div className="symptom-card-head">
                            <div className="field">
                                <label>Symptom</label>
                                <input
                                    type="text"
                                    placeholder="e.g. chest pain"
                                    value={symptom.name}
                                    onChange={(e) =>
                                        updateSymptom(
                                            index,
                                            "name",
                                            e.target.value
                                        )
                                    }
                                />
                            </div>
                            <button
                                type="button"
                                className="icon-btn"
                                title="Remove symptom"
                                onClick={() => removeSymptom(index)}
                            >
                                ✕
                            </button>
                        </div>

                        <div className="slider-field">
                            <div className="slider-top">
                                <span className="field-label">
                                    Pain / severity
                                </span>
                                <span className="slider-value">
                                    {symptom.severity}
                                    <small>
                                        {" "}
                                        / 10 ·{" "}
                                        {SEVERITY_LABELS[symptom.severity]}
                                    </small>
                                </span>
                            </div>
                            <input
                                type="range"
                                min="0"
                                max="10"
                                step="1"
                                value={symptom.severity}
                                onChange={(e) =>
                                    updateSymptom(
                                        index,
                                        "severity",
                                        Number(e.target.value)
                                    )
                                }
                            />
                            <div className="scale-marks">
                                <span>0</span>
                                <span>5</span>
                                <span>10</span>
                            </div>
                        </div>

                        <div className="field" style={{ marginTop: 14 }}>
                            <label>Duration</label>
                            <div className="input-suffix">
                                <input
                                    type="number"
                                    placeholder="How long?"
                                    min="0"
                                    value={symptom.duration_minutes}
                                    onChange={(e) =>
                                        updateSymptom(
                                            index,
                                            "duration_minutes",
                                            e.target.value
                                        )
                                    }
                                />
                                <span>min</span>
                            </div>
                        </div>
                    </div>
                ))}

                <button
                    type="button"
                    className="btn btn-ghost btn-sm"
                    onClick={() => addSymptom()}
                >
                    + Add another symptom
                </button>
            </div>

            {/* VITALS ------------------------------------------------- */}
            <div className="form-section">
                <div className="section-label">
                    <span className="num">3</span> Vital signs
                </div>
                <div className="vitals-grid">
                    <div className="field">
                        <label>Heart rate</label>
                        <div className="input-suffix">
                            <input
                                type="number"
                                placeholder="e.g. 80"
                                value={heartRate}
                                onChange={(e) =>
                                    setHeartRate(e.target.value)
                                }
                            />
                            <span>bpm</span>
                        </div>
                    </div>
                    <div className="field">
                        <label>Oxygen saturation</label>
                        <div className="input-suffix">
                            <input
                                type="number"
                                placeholder="e.g. 98"
                                value={oxygenSaturation}
                                onChange={(e) =>
                                    setOxygenSaturation(e.target.value)
                                }
                            />
                            <span>%</span>
                        </div>
                    </div>
                    <div className="field">
                        <label>Systolic BP</label>
                        <div className="input-suffix">
                            <input
                                type="number"
                                placeholder="e.g. 120"
                                value={systolicBp}
                                onChange={(e) =>
                                    setSystolicBp(e.target.value)
                                }
                            />
                            <span>mmHg</span>
                        </div>
                    </div>
                    <div className="field">
                        <label>Diastolic BP</label>
                        <div className="input-suffix">
                            <input
                                type="number"
                                placeholder="e.g. 80"
                                value={diastolicBp}
                                onChange={(e) =>
                                    setDiastolicBp(e.target.value)
                                }
                            />
                            <span>mmHg</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* CONTEXT ------------------------------------------------ */}
            <div className="form-section">
                <div className="section-label">
                    <span className="num">4</span> Clinical context
                </div>
                <div className="field">
                    <textarea
                        placeholder="History, allergies, observations, anything relevant…"
                        rows="3"
                        value={clinicalContext}
                        onChange={(e) =>
                            setClinicalContext(e.target.value)
                        }
                    />
                </div>
            </div>

            <div className="submit-bar">
                <button
                    type="submit"
                    className="btn btn-primary btn-lg btn-block"
                >
                    Assess patient →
                </button>
            </div>
        </form>
    );
}

export default PatientForm;
