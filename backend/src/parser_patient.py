from generic_parser import MedicalDocParser
import re

class PatientDetailsParser(MedicalDocParser):

    def __init__(self, text):
        super().__init__(text)

    def get_field(self, pattern, flags=0):
        match = re.findall(pattern, self.text, flags=flags)
        if len(match) > 0:
            return match[0].strip()
        
    def parse(self):
        return {
            'patient_name': self.get_field(r'Birth Date\s*\n([A-Za-z ]+?)\s+[A-Za-z]+\s+\d{1,2}\s+\d{4}'),
            'phone_number': self.get_field(r'(\(\d{3}\)\s*\d{3}-\d{4})'),
            'hepatitis_b_vaccination': self.get_field(
                r'Have you had the Hepatitis B vaccination\?\s*(.*?)\s*List any Medical Problems',
                flags=re.DOTALL
            ),
            'medical_problems': self.get_field(
                r'List any Medical Problems.*?:\s*(.*)',
                flags=re.DOTALL
            )
        }
        
        
if __name__ == '__main__':
    t = '''
   a

Patient Medical Record

Patient Information
Jerry Lucas

(279) 920-8204
4218 Wheeler Ridge Dr

Buffalo, New York, 14201
United States

In Case of Emergency

Birth Date
May 2 1998

Weight:
57

Height:
170

Joe Lucas
...

any Medical Problems (asthma, seizures, headaches):
    
    '''
    pp = PatientDetailsParser(t)
    print(pp.parse())