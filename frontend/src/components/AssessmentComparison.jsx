function AssessmentComparison(
    {
        triageResult,
        aiAssessment
    }
) {

    if (
        !triageResult ||
        !aiAssessment
    ) {

        return null;

    }


    const engineGroup = Number(
        triageResult.suggested_group
    );


    const aiGroup = Number(
        aiAssessment.severity
    );


    const matches = (

        engineGroup ===
        aiGroup

    );


    return (

        <section

            className={
                matches

                    ? "assessment-comparison match"

                    : "assessment-comparison mismatch"
            }

        >

            <div
                className="comparison-icon"
            >

                {

                    matches

                        ? "✓"

                        : "⚠"

                }

            </div>


            <div>

                <h3>

                    {

                        matches

                            ? "Both assessments align"

                            : "Assessment disagreement"

                    }

                </h3>


                <p>

                    {

                        matches

                            ? (

                                <>
                                    The deterministic engine
                                    and AI assessment suggest
                                    the same triage group.
                                </>

                            )

                            : (

                                <>
                                    The deterministic engine
                                    and AI assessment suggest
                                    different triage groups.
                                    Human review is required.
                                </>

                            )

                    }

                </p>

            </div>

        </section>

    );

}


export default AssessmentComparison;