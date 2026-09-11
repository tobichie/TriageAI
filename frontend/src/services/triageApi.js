const API_URL =
    "http://127.0.0.1:8000";


export async function assessPatient(
    patientData
) {

    const response =
        await fetch(

            `${API_URL}/triage`,

            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    patientData
                )
            }
        );


    if (!response.ok) {

        throw new Error(
            "Failed to assess patient."
        );
    }


    return await response.json();
}