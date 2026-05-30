from parser_patient import PatientDetailsParser
from parser_prescription import PrescriptionParser
from extractor import extract


def processing_pipeline(file_path, file_format):
    documents = extract(file_path, file_format)
    if file_format == 'prescription':
        doc = PrescriptionParser(documents)
        result = doc.parse()
        return result
    else:
        doc = PatientDetailsParser(documents)
        result = doc.parse()
        return result
    

print(processing_pipeline('resources/patient_details/pd_2.pdf','patient'))