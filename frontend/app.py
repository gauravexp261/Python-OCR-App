import streamlit as st
import requests

st.set_page_config(
    page_title="Medical OCR",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Medical OCR")
st.caption("Extract structured data from medical PDFs")

PATIENT_FIELDS = {
    "Patient Name": "patient_name",
    "Phone Number": "phone_number",
    "Vaccination": "hepatitis_b_vaccination",
    "Medical Problems": "medical_problems"
}

PRESCRIPTION_FIELDS = {
    "Patient Name": "patient_name",
    "Address": "patient_address",
    "Medicine": "patient_medicine",
    "Directions": "patient_directions",
    "Refills": "patient_refill"
}

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

file_format = st.selectbox(
    "Document Type",
    ["patient", "prescription"]
)

if st.button("Extract Data"):

    if uploaded_file is None:
        st.warning("Please upload a PDF file.")
        st.stop()

    try:

        with st.spinner("Extracting information..."):

            response = requests.post(
                "http://127.0.0.1:8000/process",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                },
                data={
                    "file_format": file_format
                }
            )

        if response.status_code != 200:
            st.error(f"API Error: {response.status_code}")
            st.text(response.text)
            st.stop()

        result = response.json()

        # If backend returns:
        # {"status":"success","data": {...}}
        if "data" in result:
            result = result["data"]

        st.success("Extraction Complete")

        if file_format == "patient":
            st.subheader("👤 Patient Details")
            fields = PATIENT_FIELDS
        else:
            st.subheader("📋 Prescription Details")
            fields = PRESCRIPTION_FIELDS

        col1, col2 = st.columns(2)

        items = list(fields.items())

        for label, key in fields.items():
            value = result.get(key, "N/A") or "N/A"
            st.markdown(f"**{label}**")
            st.info(value)
        ####################################
        with st.expander("Raw JSON"):
            st.json(result)

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI.\n\n"
            "Run backend first:\n\n"
            "uvicorn backend:app --reload"
        )