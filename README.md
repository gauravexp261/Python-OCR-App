# 🏥 Medical OCR System

## Overview
```text
The goal of this project is have hands on Python project (Modular coding, FastAPI endpoint, Streamlit App).
Medical OCR System is an end-to-end document processing application that extracts structured information from medical documents such as patient records and prescriptions. The application uses OCR (Optical Character Recognition) to extract text from uploaded documents and then applies custom parsing logic using Python Regular Expressions to convert unstructured text into structured JSON output.
Th regex is aligned only to type of PDFs present in resources folder.
```

---
## Project Architecture

```text
Medical Document
        │
        ▼
 OCR Extraction (pdf2image for PDF to image, OpenCV for image processing, pytesseract for image to text)
        │
        ▼
 Custom Parsers (Used Regex to extract usefull text)
        │
        ├── PatientDetailsParser
        └── PrescriptionParser
        │
        ▼
 Structured JSON Output
        │
        ▼
 FastAPI / Streamlit UI
```

---

## Project Structure

```text
OCR/
│
├── backend/
│   ├── app.py
│   ├── extractor.py
│   ├── parser_patient.py
│   ├── parser_prescription.py
│   ├── generic_parser.py
│   └── logger.py
│
├── frontend/
│   └── app.py
│
├── resources/
│   ├── patient_details/
│   └── prescription/
│
├── requirements.txt
└── README.md
```

---

## Learning Outcomes

This project helped in understanding:

* OCR Pipelines
* Text Extraction
* Regex-Based Information Parsing
* REST API Development
* FastAPI
* Streamlit
* Logging and Error Handling
* End-to-End AI Application Development

---

## Author

**Gaurav Malik**

