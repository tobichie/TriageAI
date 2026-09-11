import "./App.css";


import AIAssessment from
    "./components/AIAssessment";

import AssessmentComparison from
    "./components/AssessmentComparison";

import AIExplanation from
    "./components/AIExplanation";

import TriageResult from
    "./components/TriageResult";

import PatientForm from
    "./components/PatientForm";


import {

    useState

} from "react";


import {

    assessPatient

} from "./services/triageApi";


function App() {


    const [

        triageData,

        setTriageData

    ] = useState(null);


    const [

        loading,

        setLoading

    ] = useState(false);


    const [

        error,

        setError

    ] = useState(null);


    async function handlePatientSubmit(

        patientData

    ) {


        try {

            setLoading(true);

            setError(null);


            const triageResult =
                await assessPatient(
                    patientData
                );


            setTriageData(
                triageResult
            );

        }


        catch (

            error

        ) {

            setError(
                error.message
            );

        }


        finally {

            setLoading(false);

        }

    }


    return (

        <div
            className="app"
        >


            {/* ============================== */}
            {/* HEADER                        */}
            {/* ============================== */}

            <header
                className="app-header"
            >

                <div
                    className="app-brand"
                >

                    <div
                        className="logo"
                    >

                        T

                    </div>


                    <div>

                        <h1>
                            TriageAI
                        </h1>


                        <p>

                            Clinical Triage
                            Decision Support System

                        </p>

                    </div>

                </div>


                <div
                    className="system-status"
                >

                    <span
                        className="status-dot"
                    />

                    System Ready

                </div>

            </header>


            {/* ============================== */}
            {/* MAIN TWO COLUMN LAYOUT         */}
            {/* ============================== */}

            <main
                className="main-layout"
            >


                {/* ========================== */}
                {/* LEFT COLUMN                */}
                {/* ========================== */}

                <aside>

                    <PatientForm

                        onSubmit={
                            handlePatientSubmit
                        }

                    />

                </aside>


                {/* ========================== */}
                {/* RIGHT COLUMN               */}
                {/* ========================== */}

                <section
                    className="results-container"
                >


                    {

                        loading && (

                            <div
                                className="loading-card"
                            >

                                Assessing patient...

                            </div>

                        )

                    }


                    {

                        error && (

                            <div
                                className="error-card"
                            >

                                <strong>
                                    Assessment Error
                                </strong>


                                <p>

                                    {error}

                                </p>

                            </div>

                        )

                    }


                    {

                        !triageData &&
                        !loading &&
                        !error && (

                            <div
                                className="empty-results"
                            >

                                <div
                                    className="empty-icon"
                                >

                                    +

                                </div>


                                <h2>

                                    Ready for Assessment

                                </h2>


                                <p>

                                    Enter the patient's
                                    information and vital signs
                                    to generate a structured
                                    triage assessment.

                                </p>

                            </div>

                        )

                    }


                    {

                        triageData && (

                            <>


                                <div
                                    className="results-header"
                                >

                                    <h2>

                                        Triage Assessment

                                    </h2>


                                    <p>

                                        Deterministic and
                                        AI-supported assessment

                                    </p>

                                </div>


                                {/* ================== */}
                                {/* TWO RESULT CARDS   */}
                                {/* ================== */}

                                <div
                                    className="assessment-grid"
                                >

                                    <TriageResult

                                        result={
                                            triageData
                                                .triage_result
                                        }

                                    />


                                    <AIAssessment

                                        assessment={
                                            triageData
                                                .ai_assessment
                                        }

                                    />

                                </div>


                                {/* ================== */}
                                {/* COMPARISON         */}
                                {/* ================== */}

                                <AssessmentComparison

                                    triageResult={
                                        triageData
                                            .triage_result
                                    }

                                    aiAssessment={
                                        triageData
                                            .ai_assessment
                                    }

                                />


                                {/* ================== */}
                                {/* AI EXPLANATION     */}
                                {/* ================== */}

                                <AIExplanation

                                    explanation={
                                        triageData
                                            .ai_explanation
                                    }

                                />


                            </>

                        )

                    }


                </section>

            </main>

        </div>

    );

}


export default App;