import {
    useState
} from "react";


function AIExplanation(
    {
        explanation
    }
) {

    const [

        isExpanded,

        setIsExpanded

    ] = useState(false);


    if (
        !explanation
    ) {

        return null;

    }


    const paragraphs = (
        explanation
            .split("\n\n")
            .filter(
                paragraph =>
                    paragraph.trim()
            )
    );


    return (

        <section
            className="ai-explanation"
        >

            <div
                className="section-header"
            >

                <div>

                    <h2>
                        AI Explanation
                    </h2>

                    <p>
                        Explanation of the deterministic
                        engine result.
                    </p>

                </div>


                <button

                    className="expand-button"

                    onClick={
                        () =>

                            setIsExpanded(
                                !isExpanded
                            )
                    }

                >

                    {

                        isExpanded

                            ? "Show less"

                            : "Show explanation"

                    }

                </button>

            </div>


            {

                isExpanded && (

                    <div
                        className="explanation-content"
                    >

                        {

                            paragraphs.map(

                                (
                                    paragraph,
                                    index
                                ) => (

                                    <p
                                        key={index}
                                    >

                                        {
                                            formatText(
                                                paragraph
                                            )
                                        }

                                    </p>

                                )

                            )

                        }

                    </div>

                )

            }


            <div
                className="ai-warning"
            >

                ⚠ AI-generated explanation.
                It explains the deterministic
                system output and does not
                constitute a clinical decision.

            </div>

        </section>

    );

}


function formatText(
    text
) {

    return (

        text

            .replace(
                /## /g,
                ""
            )

            .replace(
                /\*\*/g,
                ""
            )

            .replace(
                /^- /gm,
                ""
            )

    );

}


export default AIExplanation;