from generic_parser import MedicalDocParser
import re
from logging_setup import setup_logger

logger = setup_logger('parser_PrescriptionParser')

class PrescriptionParser(MedicalDocParser):
    def __init__(self, text):
        try:
            super().__init__(text)
            logger.info("PrescriptionParser initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PrescriptionParser: {e}")
            raise
    
        
    def get_field(self,pattern, flags = 0):
        try:
            match = re.findall(pattern, self.text,flags=flags)
            if match:
                logger.info(f'get_field ran and recieved match')
                if len(match) > 0:
                    return match[0].strip() 
            else:
                logger.info(f'get_field ran but did not recieved any match')
        except Exception as e:
            logger.error(f" Unexpected error  in get field {e}")
        
    def parse(self):
        try:
            parsed_data =  {'patient_name':self.get_field('Name:(.*)Date:'),
                    'patient_address':self.get_field('Address:(.*)\n'),
                    'patient_medicine':self.get_field('Address[^\n]*(.*)Directions', flags =re.DOTALL),
                    'patient_directions':self.get_field('Directions[^\n]*(.*)Refill', flags =re.DOTALL),
                    'patient_refill':self.get_field('Refill:(.*)times', flags = 0)
                    }
            if parsed_data:
                logger.info(f'data parsed')
            return parsed_data
        except Exception as e:
            logger.error(f" Unexpected error while parsing {e}")

        
   
# if __name__ == '__main__':
#     t = '''
#     Dr John Smith, M.D
# 2 Non-Important Street,
# New York, Phone (000)-111-2222

# Name: Marta Sharapova Date: 5/11/2022

# Address: 9 tennis court, new Russia, DC

# K

# Prednisone 20 mg
# Lialda 2.4 gram

# Directions:

# Prednisone, Taper 5 mig every 3 days,
# Finish in 2.5 weeks a
# Lialda - take 2 pill everyday for 1 month

# Refill: 2 times
    
#     '''
#     pp = PrescriptionParser(t)
#     print(pp.parse())