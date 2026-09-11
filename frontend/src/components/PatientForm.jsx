import {

    useState

} from "react";


function parseSymptoms(
    symptoms
) {

    return symptoms.flatMap(

        (symptom) => {

            const symptomNames = (

                symptom.name

                    .split(",")

                    .map(

                        (name) =>

                            name.trim()

                    )

                    .filter(

                        (name) =>

                            name.length > 0

                    )

            );


            return symptomNames.map(

                (name) => (

                    {

                        name: name,


                        severity:

                            symptom.severity === ""

                                ? null

                                : Number(
                                    symptom.severity
                                ),


                        duration_minutes:

                            symptom.duration_minutes === ""

                                ? null

                                : Number(
                                    symptom.duration_minutes
                                )

                    }

                )

            );

        }

    );

}

function PatientForm(
    {
        onSubmit
    }
) {


    const [

        age,

        setAge

    ] = useState("");


    const [

        clinicalContext,

        setClinicalContext

    ] = useState("");


    const [

        heartRate,

        setHeartRate

    ] = useState("");


    const [

        oxygenSaturation,

        setOxygenSaturation

    ] = useState("");


    const [

        systolicBp,

        setSystolicBp

    ] = useState("");


    const [

        diastolicBp,

        setDiastolicBp

    ] = useState("");


    const [

        symptoms,

        setSymptoms

    ] = useState([

        {

            name: "",

            severity: "",

            duration_minutes: ""

        }

    ]);


    function handleSymptomChange(

        index,

        field,

        value

    ) {

        const updatedSymptoms = [

            ...symptoms

        ];


        updatedSymptoms[index][field] =
            value;


        setSymptoms(
            updatedSymptoms
        );

    }


    function addSymptom() {

        setSymptoms([

            ...symptoms,

            {

                name: "",

                severity: "",

                duration_minutes: ""

            }

        ]);

    }


    function removeSymptom(
        index
    ) {

        const updatedSymptoms =
            symptoms.filter(

                (

                    _,

                    symptomIndex

                ) =>

                    symptomIndex !== index

            );


        setSymptoms(
            updatedSymptoms
        );

    }


    function handleSubmit(
        event
    ) {

        event.preventDefault();


        const patientData = {


            age:

                Number(age),


            symptoms:

                parseSymptoms(

                    symptoms.filter(

                        (
                            symptom
                        ) =>

                            symptom.name.trim() !== ""

                    )

                ),

            vital_signs: {


                heart_rate:

                    heartRate === ""

                        ? null

                        : Number(
                            heartRate
                        ),


                oxygen_saturation:

                    oxygenSaturation === ""

                        ? null

                        : Number(
                            oxygenSaturation
                        ),


                systolic_bp:

                    systolicBp === ""

                        ? null

                        : Number(
                            systolicBp
                        ),


                diastolic_bp:

                    diastolicBp === ""

                        ? null

                        : Number(
                            diastolicBp
                        )

            },


            clinical_context:

                clinicalContext || null

        };


        onSubmit(
            patientData
        );

    }


    return (

        <form

            className="patient-form"

            onSubmit={
                handleSubmit
            }

        >


            {/* ========================== */}
            {/* FORM HEADER                */}
            {/* ========================== */}

            <div
                className="form-header"
            >

                <h2>

                    Patient Assessment

                </h2>


                <p>

                    Enter available patient
                    information.

                </p>

            </div>


            {/* ========================== */}
            {/* PATIENT INFORMATION        */}
            {/* ========================== */}

            <div
                className="form-section"
            >

                <div
                    className="form-section-title"
                >

                    Patient Information

                </div>


                <div
                    className="form-group"
                >

                    <label>

                        Age

                    </label>


                    <input

                        type="number"

                        placeholder="Age"

                        min="0"

                        value={age}

                        onChange={

                            (
                                event
                            ) =>

                                setAge(
                                    event.target.value
                                )

                        }

                        required

                    />

                </div>

            </div>


            {/* ========================== */}
            {/* SYMPTOMS                   */}
            {/* ========================== */}

            <div
                className="form-section"
            >

                <div
                    className="form-section-title"
                >

                    Symptoms

                </div>


                {

                    symptoms.map(

                        (

                            symptom,

                            index

                        ) => (

                            <div

                                className="symptom-card"

                                key={index}

                            >


                                <div
                                    className="form-group"
                                >

                                    <label>

                                        Symptom

                                    </label>


                                    <input

                                        type="text"

                                        placeholder="e.g. chest pain"

                                        value={
                                            symptom.name
                                        }

                                        onChange={

                                            (
                                                event
                                            ) =>

                                                handleSymptomChange(

                                                    index,

                                                    "name",

                                                    event.target.value

                                                )

                                        }

                                    />

                                </div>


                                <div
                                    className="form-row"
                                >


                                    <div
                                        className="form-group"
                                    >

                                        <label>

                                            Severity

                                        </label>


                                        <input

                                            type="number"

                                            placeholder="1–10"

                                            min="1"

                                            max="10"

                                            value={
                                                symptom.severity
                                            }

                                            onChange={

                                                (
                                                    event
                                                ) =>

                                                    handleSymptomChange(

                                                        index,

                                                        "severity",

                                                        event.target.value

                                                    )

                                            }

                                        />

                                    </div>


                                    <div
                                        className="form-group"
                                    >

                                        <label>

                                            Duration

                                        </label>


                                        <input

                                            type="number"

                                            placeholder="Minutes"

                                            min="0"

                                            value={

                                                symptom
                                                    .duration_minutes

                                            }

                                            onChange={

                                                (
                                                    event
                                                ) =>

                                                    handleSymptomChange(

                                                        index,

                                                        "duration_minutes",

                                                        event.target.value

                                                    )

                                            }

                                        />

                                    </div>


                                </div>


                                {

                                    symptoms.length > 1 && (

                                        <button

                                            className="remove-symptom-button"

                                            type="button"

                                            onClick={

                                                () =>

                                                    removeSymptom(
                                                        index
                                                    )

                                            }

                                        >

                                            Remove symptom

                                        </button>

                                    )

                                }


                            </div>

                        )

                    )

                }


                <button

                    className="add-symptom-button"

                    type="button"

                    onClick={
                        addSymptom
                    }

                >

                    + Add Symptom

                </button>


            </div>


            {/* ========================== */}
            {/* VITAL SIGNS                */}
            {/* ========================== */}

            <div
                className="form-section"
            >

                <div
                    className="form-section-title"
                >

                    Vital Signs

                </div>


                <div
                    className="vitals-grid"
                >


                    <div
                        className="form-group"
                    >

                        <label>

                            Heart Rate
                            (BPM)

                        </label>


                        <input

                            type="number"

                            placeholder="e.g. 80"

                            value={heartRate}

                            onChange={

                                (
                                    event
                                ) =>

                                    setHeartRate(
                                        event.target.value
                                    )

                            }

                        />

                    </div>


                    <div
                        className="form-group"
                    >

                        <label>

                            Oxygen Saturation
                            (%)

                        </label>


                        <input

                            type="number"

                            placeholder="e.g. 98"

                            value={
                                oxygenSaturation
                            }

                            onChange={

                                (
                                    event
                                ) =>

                                    setOxygenSaturation(
                                        event.target.value
                                    )

                            }

                        />

                    </div>


                    <div
                        className="form-group"
                    >

                        <label>

                            Systolic BP

                        </label>


                        <input

                            type="number"

                            placeholder="e.g. 120"

                            value={systolicBp}

                            onChange={

                                (
                                    event
                                ) =>

                                    setSystolicBp(
                                        event.target.value
                                    )

                            }

                        />

                    </div>


                    <div
                        className="form-group"
                    >

                        <label>

                            Diastolic BP

                        </label>


                        <input

                            type="number"

                            placeholder="e.g. 80"

                            value={diastolicBp}

                            onChange={

                                (
                                    event
                                ) =>

                                    setDiastolicBp(
                                        event.target.value
                                    )

                            }

                        />

                    </div>


                </div>

            </div>


            {/* ========================== */}
            {/* CLINICAL CONTEXT           */}
            {/* ========================== */}

            <div
                className="form-section"
            >

                <div
                    className="form-section-title"
                >

                    Clinical Context

                </div>


                <div
                    className="form-group"
                >

                    <textarea

                        placeholder={
                            "Additional clinical context"
                        }

                        rows="4"

                        value={
                            clinicalContext
                        }

                        onChange={

                            (
                                event
                            ) =>

                                setClinicalContext(
                                    event.target.value
                                )

                        }

                    />

                </div>

            </div>


            <button

                className="assess-button"

                type="submit"

            >

                Assess Patient

            </button>


        </form>

    );

}


export default PatientForm;