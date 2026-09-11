function AIAssessment(
    {
        assessment
    }
) {

    if (
        !assessment
    ) {

        return null;

    }


    return (

        <section
            className="ai-assessment"
        >

            <div
                className="assessment-header"
            >

                <div
                    className="assessment-icon"
                >

                    ✦

                </div>


                <div>

                    <h2>
                        AI Assessment
                    </h2>

                    <p>
                        Independent AI assessment
                    </p>

                </div>

            </div>


            <div
                className="ai-group-card"
            >

                <span>
                    Suggested Group
                </span>


                <strong>

                    {
                        assessment.severity
                    }

                </strong>

            </div>


            <div
                className="ai-reason"
            >

                <div
                    className="reason-header"
                >

                    <h3>
                        AI Reasoning
                    </h3>

                </div>


                <p>

                    {
                        assessment.reason
                    }

                </p>

            </div>


            <p
                className="ai-disclaimer"
            >

                Independent AI assessment.
                Does not override the
                deterministic result.

            </p>

        </section>

    );

}


export default AIAssessment;