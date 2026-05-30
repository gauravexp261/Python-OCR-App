from generic_parser import MedicalDocParser
import re


class PatientDetailsParser(MedicalDocParser):

    def __init__(self, text):
        super().__init__(text)

    def get_field(self, pattern, flags=0):
        match = re.search(pattern, self.text, flags=flags)

        if match:
            return match.group(1).strip()

        return None

    def remove_noise_from_name(self, name):
        if not name:
            return None

        name = name.replace("Birth Date", "").strip()

        date_pattern = r'((Jan|Feb|March|April|May|June|July|Aug|Sep|Oct|Nov|Dec)[ \d]+)'
        date_matches = re.findall(date_pattern, name)

        if date_matches:
            date = date_matches[0][0]
            name = name.replace(date, '').strip()

        return name

    def clean_medical_problem(self, text):
        if not text:
            return None

        lines = [line.strip() for line in text.split('\n') if line.strip()]

        if lines:
            return lines[0]

        return None

    def parse(self):
        patient_name = self.get_field(
            r'Patient Information\s*(.*?)\s*\(\d{3}\)',
            flags=re.DOTALL
        )

        medical_problem = self.get_field(
            r'List any Medical Problems.*?:\s*(.*?)(?=Name of Insurance Company|Medical Insurance Details)',
            flags=re.DOTALL
        )

        return {
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