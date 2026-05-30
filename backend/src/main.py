from parser_patient import PatientDetailsParser
from parser_prescription import PrescriptionParser
from extractor import extract
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
from pydantic import BaseModel
import shutil



app = FastAPI()
UPLOAD_DIR = 'resources'
os.makedirs(UPLOAD_DIR, exist_ok=True)



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
    
@app.post('/process')
def process(file: UploadFile = File(...), file_format: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = processing_pipeline(file_path, file_format)
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        if os.path.exists(file_path):  # Clean up uploaded file
            os.remove(file_path)
    


        
#print(processing_pipeline('resources/prescription/pre_2.pdf','prescription'))