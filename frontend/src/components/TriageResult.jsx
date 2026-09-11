function TriageResult(
    {
        result
    }
) {

    return (

        <section
            className="triage-result"
        >

            <h2>
                Triage Result
            </h2>


            <div
                className="triage-summary"
            >

                <div
                    className="triage-group"
                >

                    <span>
                        Suggested Group
                    </span>


                    <strong>
                        {
                            result.suggested_group
                        }
                    </strong>

                </div>


                <div>

                    <strong>
                        {
                            result.treatment_priority
                        }
                    </strong>

                </div>

            </div>


            <div
                className="triage-details"
            >

                <p>

                    <strong>
                        Maximum Wait:
                    </strong>

                    {" "}

                    {
                        result.max_wait_minutes
                    }

                    {" "}
                    minutes

                </p>


                <p>

                    <strong>
                        Reevaluation:
                    </strong>

                    {" "}

                    {
                        result.reevaluation_minutes
                    }

                    {" "}
                    minutes

                </p>

            </div>


            <RuleFindings
                findings={
                    result.rule_findings
                }
            />


            <TriggeredRules
                rules={
                    result.triggered_rules
                }
            />


            <RedFlags
                flags={
                    result.red_flags
                }
            />


            <RelevantFactors
                factors={
                    result.relevant_factors
                }
            />


            <SafetyInformation
                result={result}
            />

        </section>

    );

}


function RuleFindings(
    {
        findings
    }
) {

    if (
        !findings ||
        findings.length === 0
    ) {

        return null;

    }


    return (

        <section
            className="result-section"
        >

            <h3>
                Rule Findings
            </h3>


            {

                findings.map(

                    (
                        finding,
                        index
                    ) => (

                        <div
                            key={index}
                            className="finding-card"
                        >

                            <strong>

                                {
                                    finding.rule_id
                                }

                            </strong>


                            <p>

                                {
                                    finding.description
                                }

                            </p>


                            {

                                finding.observed_value !==
                                null && (

                                    <p>

                                        Observed:

                                        {" "}

                                        {
                                            String(
                                                finding.observed_value
                                            )
                                        }

                                    </p>

                                )

                            }


                            {

                                finding.threshold !==
                                null && (

                                    <p>

                                        Threshold:

                                        {" "}

                                        {
                                            String(
                                                finding.threshold
                                            )
                                        }

                                    </p>

                                )

                            }

                        </div>

                    )

                )

            }

        </section>

    );

}


function TriggeredRules(
    {
        rules
    }
) {

    if (
        !rules ||
        rules.length === 0
    ) {

        return null;

    }


    return (

        <section
            className="result-section"
        >

            <h3>
                Triggered Rules
            </h3>


            <ul>

                {

                    rules.map(

                        (
                            rule,
                            index
                        ) => (

                            <li
                                key={index}
                            >

                                {rule}

                            </li>

                        )

                    )

                }

            </ul>

        </section>

    );

}


function RedFlags(
    {
        flags
    }
) {

    if (
        !flags ||
        flags.length === 0
    ) {

        return null;

    }


    return (

        <section
            className="result-section red-flags"
        >

            <h3>
                Red Flags
            </h3>


            <ul>

                {

                    flags.map(

                        (
                            flag,
                            index
                        ) => (

                            <li
                                key={index}
                            >

                                {flag}

                            </li>

                        )

                    )

                }

            </ul>

        </section>

    );

}


function RelevantFactors(
    {
        factors
    }
) {

    if (
        !factors ||
        factors.length === 0
    ) {

        return null;

    }


    return (

        <section
            className="result-section"
        >

            <h3>
                Relevant Factors
            </h3>


            <ul>

                {

                    factors.map(

                        (
                            factor,
                            index
                        ) => (

                            <li
                                key={index}
                            >

                                {factor}

                            </li>

                        )

                    )

                }

            </ul>

        </section>

    );

}


function SafetyInformation(
    {
        result
    }
) {

    return (

        <section
            className="result-section safety-information"
        >

            <h3>
                Safety Information
            </h3>


            <p>

                <strong>
                    Assessment Status:
                </strong>

                {" "}

                {
                    String(
                        result.assessment_status
                    )
                }

            </p>


            {

                result.requires_human_review && (

                    <p>

                        ⚠ Human clinical review
                        required.

                    </p>

                )

            }


            {

                result.safety_warnings &&
                result.safety_warnings.length > 0 && (

                    <ul>

                        {

                            result.safety_warnings.map(

                                (
                                    warning,
                                    index
                                ) => (

                                    <li
                                        key={index}
                                    >

                                        {warning}

                                    </li>

                                )

                            )

                        }

                    </ul>

                )

            }

        </section>

    );

}


export default TriageResult;