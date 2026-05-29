from backend.src.generic_parser import MedicalDocParser
import re

class PrescriptionParser(MedicalDocParser):
    def __init__(self, text):
        super().__init__(text)
        
    def parse(self):
        return {'patient_name':self.get_name(),
                'patient_address':self.get_address(),
                'patient_medicine':self.get_medicine(),
                'patient_directions':self.get_directions(),
                'patient_refill':self.get_refill()
                }
        
    def get_field(self,field_name):
        if 

    def get_name(self):
        pattern = 'Name:(.*)Date:'
        match = re.findall(pattern, self.text)
        if len(match) > 0:
            return match[0].strip()
        
    def get_address(self):
        pattern = 'Address:(.*)\n'
        match = re.findall(pattern, self.text)
        if len(match) > 0:
            return match[0].strip()
        
    def get_medicine(self):
        pattern = 'Address[^\n]*(.*)Directions'
        match = re.findall(pattern, self.text,flags=re.DOTALL)
        if len(match) > 0:
            return match[0].strip()
        
    def get_directions(self):
        pattern = 'Directions[^\n]*(.*)Refill'
        match = re.findall(pattern, self.text,flags=re.DOTALL)
        if len(match) > 0:
            return match[0].strip()
        
        
    def get_refill(self):
        pattern = 'Refill:(.*)times'
        match = re.findall(pattern, self.text)
        if len(match) > 0:
            return match[0].strip()
    
    
    
if __name__ == '__main__':
    t = 'Name: Gadfffa  Date:23311'
    pp = PrescriptionParser(t)
    print(pp.parse())