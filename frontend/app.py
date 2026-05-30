import streamlit as st
import requests

st.set_page_config(page_title="Medical OCR", page_icon="🏥", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
            background-color: #f5f3ef;
            color: #1a1a1a;
        }
        .title {
            font-family: 'DM Serif Display', serif;
            font-size: 2.4rem;
            color: #1a1a1a;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            font-size: 0.95rem;
            color: #888;
            margin-bottom: 2rem;
        }
        .section-header {
            font-family: 'DM Serif Display', serif;
            font-size: 1.2rem;
            color: #1a1a1a;
            margin-bottom: 1rem;
            padding-bottom: 0.4rem;
            border-bottom: 2px solid #f0ede8;
        }
        .card {
            background: #ffffff;
            border-radius: 16px;
            padding: 2rem;
            margin-top: 1.5rem;
            box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        }
        .field-label {
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #aaa;
            margin-bottom: 0.2rem;
        }
        .field-value {
            font-size: 1rem;
            font-weight: 500;
            color: #1a1a1a;
            margin-bottom: 1.2rem;
        }
        .badge {
            display: inline-block;
            background: #e8f5e9;
            color: #2e7d32;
            border-radius: 999px;
            padding: 2px 14px;
            font-size: 0.88rem;
            font-weight: 500;
        }
        .badge-na {
            background: #f3f3f3;
            color: #999;
        }
        .badge-prescription {
            background: #e3f2fd;
            color: #1565c0;
        }
        div[data-testid="stFileUploader"] {
            border: 2px dashed #d0cdc7;
            border-radius: 12px;
            padding: 1rem;
            background: #fafaf8;
        }
        .stButton > button {
            background-color: #1a1a1a;
            color: white;
            border-radius: 10px;
            padding: 0.6rem 2rem;
            font-size: 1rem;
            font-family: 'DM Sans', sans-serif;
            border: none;
            width: 100%;
            margin-top: 0.5rem;
        }
        .stButton > button:hover {
            background-color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Field groupings per document type
PATIENT_FIELDS = {
    "patient_name": "Patient Name",
    "phone_number": "Phone Number",
    "hepatitis_b_vaccination": "Hepatitis B Vaccination",
    "medical_problems": "Medical Problems",
}

PRESCRIPTION_FIELDS = {
    "patient_name": "Patient Name",
    "patient_address": "Patient Address",
    "patient_medicine": "Medicine",
    "patient_directions": "Directions",
    "patient_refill": "Refills",
}

st.markdown('<div class="title">🏥 Medical OCR</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Extract structured data from medical PDFs instantly</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
file_format = st.selectbox("Document Type", ["patient", "prescription"])

if st.button("Extract Data"):
    if uploaded_file is None:
        st.warning("Please upload a PDF file first.")
    else:
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/process",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                    data={"file_format": file_format}
                )

                if response.status_code == 200:
                    result = response.json()
                    fields = PRESCRIPTION_FIELDS if file_format == "prescription" else PATIENT_FIELDS
                    badge_class = "badge badge-prescription" if file_format == "prescription" else "badge"

                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    header = "📋 Prescription Details" if file_format == "prescription" else "👤 Patient Details"
                    st.markdown(f'<div class="section-header">{header}</div>', unsafe_allow_html=True)

                    for key, label in fields.items():
                        value = result.get(key, "N/A") or "N/A"
                        is_empty = str(value).strip().upper() in ["N/A", "", "NONE"]
                        css_class = "badge badge-na" if is_empty else badge_class
                        st.markdown(f'<div class="field-label">{label}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="field-value"><span class="{css_class}">{value}</span></div>', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                    with st.expander("Raw JSON"):
                        st.json(result)

                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI. Make sure it's running at http://127.0.0.1:8000")