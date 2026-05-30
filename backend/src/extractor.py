from pdf2image import convert_from_path
import os
import pytesseract
from util import preprocess_image


#BASE_DIR = os.path.dirname(__file__)
POPPLER_PATH = r"C:\poppler-26.02.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"






def extract(file_path, file_format):
    pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
    document_text = ''
    for page in pages:
        processed_image = preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang='eng')
        document_text += '\n' + text
        
    return document_text
        
        
if __name__ == '__main__':
    data = extract('resources/prescription/pre_2.pdf','prescription')
    print(data)
        
