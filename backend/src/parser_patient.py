from generic_parser import MedicalDocParser
import re
from logging_setup import setup_logger

logger = setup_logger('parser_patient')

class PatientDetailsParser(MedicalDocParser):

    def __init__(self, text):
        try:
            super().__init__(text)
            logger.info("PatientDetailsParser initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PatientDetailsParser: {e}")
            raise

    def get_field(self, pattern, flags=0):
        try:
            match = re.search(pattern, self.text, flags=flags)
            if match:
                logger.debug(f"Field extracted for pattern{pattern}")
                return match.group(1).strip()
            logger.debug(f"No match found for pattern {pattern}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_field with pattern {pattern}")
            return None

    def remove_noise_from_name(self, name):
        try:
            if not name:
                logger.debug("remove_noise_from_name received empty or None name")
                return None

            name = name.replace("Birth Date", "").strip()

            date_pattern = r'((Jan|Feb|March|April|May|June|July|Aug|Sep|Oct|Nov|Dec)[ \d]+)'
            date_matches = re.findall(date_pattern, name)

            if date_matches:
                date = date_matches[0][0]
                name = name.replace(date, '').strip()
                logger.debug(f"removed data noise")
            return name
        except re.error as e:
            logger.error(f"Regex error while removing noise from name '{name}': {e}")
            return 
        except Exception as e:
            logger.error(f"Unexpected error in remove_noise_from_name for '{name}': {e}")
            return None
    

    def clean_medical_problem(self, text):
        try:
            if not text:
                logger.debug("clean_medical_problem received empty or None text")
                return None

            lines = [line.strip() for line in text.split('\n') if line.strip()]

            if lines:
                logger.debug(f"Cleaned medical problem, extracted first line: '{lines[0]}'")
                return lines[0]

            logger.debug("No valid lines found in medical problem text")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in clean_medical_problem: {e}")
            return None

    def parse(self):
        logger.info("Starting patient details parsing")
        try:
            patient_name = self.get_field(
                r'Patient Information\s*(.*?)\s*\(\d{3}\)',
                flags=re.DOTALL
            )

            medical_problem = self.get_field(
                r'List any Medical Problems.*?:\s*(.*?)(?=Name of Insurance Company|Medical Insurance Details)',
                flags=re.DOTALL
            )

            result =  {
                'patient_name': self.remove_noise_from_name(patient_name),

                'phone_number': self.get_field(
                    r'(\(\d{3}\)\s*\d{3}-\d{4})'
                ),

                'hepatitis_b_vaccination': self.get_field(
                    r'Have you had the Hepatitis B vaccination\?.*?(Yes|No)',
                    flags=re.DOTALL
                ),

                'medical_problems': self.clean_medical_problem(
                    medical_problem
                )
            }
            
            if result:
                logger.info(f"Parsing completed successfully.")
                return result
            else:
                logger.error(f"Fields could not be extracted")
        except Exception as e:
            logger.error(f"Critical error during parse(): {e}", exc_info=True)
            return {}


# if __name__ == '__main__':

#     t = '''
# Patient Medical Record

# Patient Information
# Jerry Lucas

# (279) 920-8204
# 4218 Wheeler Ridge Dr

# Buffalo, New York, 14201
# United States

# In Case of Emergency

# Birth Date
# May 2 1998

# Weight:
# 57

# Height:
# 170

# Joe Lucas
# '''

#     pp = PatientDetailsParser(t)
#     print(pp.parse())