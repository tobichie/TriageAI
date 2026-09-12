const API_URL =
    "http://192.168.178.123:8000"; // This needs to be changed to whatever ip you can reach your device under


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