import { useEffect, useState } from "react";

import "./App.css";

import PatientForm from "./components/PatientForm";
import AssessmentResult from "./components/AssessmentResult";
import Board from "./components/Board";
import Records from "./components/Records";

import { assessPatient, checkHealth } from "./services/triageApi";
import { getPatients } from "./services/dashboardApi";

function getInitialTheme() {
    try {
        const saved = localStorage.getItem("triageai-theme");
        if (saved === "dark" || saved === "light") {
            return saved;
        }
    } catch {
        // ignore
    }
    try {
        if (
            window.matchMedia &&
            window.matchMedia("(prefers-color-scheme: dark)").matches
        ) {
            return "dark";
        }
    } catch {
        // ignore
    }
    return "light";
}

function SunIcon() {
    return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <circle cx="12" cy="12" r="4" />
            <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
        </svg>
    );
}

function MoonIcon() {
    return (
        <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
        </svg>
    );
}

function ThemeToggle({ theme, onToggle }) {
    const dark = theme === "dark";
    return (
        <button
            type="button"
            className="theme-toggle"
            role="switch"
            aria-checked={dark}
            aria-label={
                dark ? "Switch to light mode" : "Switch to dark mode"
            }
            title={dark ? "Light mode" : "Dark mode (night shift)"}
            onClick={onToggle}
        >
            <span className="knob">
                {dark ? <MoonIcon /> : <SunIcon />}
            </span>
        </button>
    );
}

function Logo() {
    return (
        <svg viewBox="0 0 24 24" fill="none">
            <path
                d="M3 12h3.5l1.5-4 3 8 2-5 1.5 1h4"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
        </svg>
    );
}

function App() {
    const [view, setView] = useState("assess");

    const [triageData, setTriageData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Data used to pre-fill the intake form (re-assess flow).
    const [prefill, setPrefill] = useState(null);
    const [formKey, setFormKey] = useState(0);

    // Waiting count shown as a badge on the Board tab.
    const [waitingCount, setWaitingCount] = useState(null);

    // Backend health: "checking" | "online" | "offline".
    const [apiStatus, setApiStatus] = useState("checking");

    useEffect(() => {
        let active = true;

        async function ping() {
            try {
                const ok = await checkHealth();
                if (active) setApiStatus(ok ? "online" : "offline");
            } catch {
                if (active) setApiStatus("offline");
            }
        }

        ping();
        const t = setInterval(ping, 15000);
        return () => {
            active = false;
            clearInterval(t);
        };
    }, []);

    // Light / dark theme (persisted).
    const [theme, setTheme] = useState(getInitialTheme);

    useEffect(() => {
        document.documentElement.setAttribute("data-theme", theme);
        try {
            localStorage.setItem("triageai-theme", theme);
        } catch {
            // ignore
        }
    }, [theme]);

    async function refreshWaiting() {
        try {
            const list = await getPatients(true);
            setWaitingCount(
                list.filter((p) => p.status !== "done").length
            );
        } catch {
            // non-critical
        }
    }

    useEffect(() => {
        refreshWaiting();
        const t = setInterval(refreshWaiting, 20000);
        return () => clearInterval(t);
    }, []);

    async function handleSubmit(patientData) {
        try {
            setLoading(true);
            setError(null);
            const result = await assessPatient(patientData);
            setTriageData(result);
            refreshWaiting();
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    }

    function handleReassess(patient) {
        setPrefill({
            name: patient.name,
            age: patient.age,
            symptoms: patient.symptoms,
            vital_signs: patient.vital_signs,
            clinical_context: patient.clinical_context,
        });
        setFormKey((k) => k + 1);
        setTriageData(null);
        setError(null);
        setView("assess");
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function goToAssess() {
        // Fresh, blank intake.
        setPrefill(null);
        setFormKey((k) => k + 1);
        setTriageData(null);
        setError(null);
        setView("assess");
    }

    const navItems = [
        { key: "assess", label: "Assess" },
        { key: "board", label: "Board", badge: waitingCount },
        { key: "records", label: "Records" },
    ];

    return (
        <div className="app">
            <header className="topbar">
                <div className="topbar-brand">
                    <div className="logo">
                        <Logo />
                    </div>
                    <div>
                        <h1>TriageAI</h1>
                        <p>Clinical triage decision support</p>
                    </div>
                </div>

                <nav className="topbar-nav">
                    {navItems.map((item) => (
                        <button
                            key={item.key}
                            className={
                                "nav-btn" +
                                (view === item.key ? " active" : "")
                            }
                            onClick={() =>
                                item.key === "assess"
                                    ? goToAssess()
                                    : setView(item.key)
                            }
                        >
                            {item.label}
                            {item.badge != null && item.badge > 0 && (
                                <span className="count">{item.badge}</span>
                            )}
                        </button>
                    ))}
                </nav>

                <div
                    style={{
                        marginLeft: "auto",
                        display: "flex",
                        alignItems: "center",
                        gap: 16,
                    }}
                >
                    <ThemeToggle
                        theme={theme}
                        onToggle={() =>
                            setTheme((t) =>
                                t === "dark" ? "light" : "dark"
                            )
                        }
                    />
                    <div
                        className={`topbar-status status-${apiStatus}`}
                        title={
                            apiStatus === "online"
                                ? "API reachable (/api/health)"
                                : apiStatus === "offline"
                                ? "API not reachable (/api/health)"
                                : "Checking API…"
                        }
                    >
                        {apiStatus === "offline" ? (
                            <>
                                <svg
                                    className="status-warn-ico"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    aria-hidden="true"
                                >
                                    <path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" />
                                </svg>
                                System not ready
                            </>
                        ) : (
                            <>
                                <span className="status-dot" />
                                {apiStatus === "online"
                                    ? "System ready"
                                    : "Checking…"}
                            </>
                        )}
                    </div>
                </div>
            </header>

            {view === "assess" && (
                <main className="page">
                    <div className="intake-layout">
                        <PatientForm
                            key={formKey}
                            onSubmit={handleSubmit}
                            initialData={prefill}
                        />

                        <div>
                            {loading && (
                                <div className="card">
                                    <div className="loading">
                                        <span className="spinner" />
                                        Assessing patient…
                                    </div>
                                </div>
                            )}

                            {error && !loading && (
                                <div className="error-banner">
                                    <span>⚠</span>
                                    <div>
                                        <strong>Assessment failed</strong>
                                        <p>{error}</p>
                                    </div>
                                </div>
                            )}

                            {!loading && !error && !triageData && (
                                <div className="card">
                                    <div className="empty">
                                        <div className="empty-ico">
                                            <svg
                                                viewBox="0 0 24 24"
                                                width="30"
                                                height="30"
                                                fill="none"
                                            >
                                                <path
                                                    d="M3 12h4l2-5 3 10 2-6 1.5 1H21"
                                                    stroke="currentColor"
                                                    strokeWidth="2"
                                                    strokeLinecap="round"
                                                    strokeLinejoin="round"
                                                />
                                            </svg>
                                        </div>
                                        <h2>Ready to assess</h2>
                                        <p>
                                            Fill in what you observe on the
                                            left. TriageAI returns a
                                            priority, the reasons behind it,
                                            and an independent AI second
                                            opinion.
                                        </p>
                                    </div>
                                </div>
                            )}

                            {!loading && triageData && (
                                <AssessmentResult data={triageData} />
                            )}
                        </div>
                    </div>
                </main>
            )}

            {view === "board" && <Board onReassess={handleReassess} />}

            {view === "records" && (
                <Records onReassess={handleReassess} />
            )}
        </div>
    );
}

export default App;
