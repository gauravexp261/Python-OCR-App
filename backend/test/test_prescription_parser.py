import pytest
import os
import sys
from backend.src.parser_prescription import PrescriptionParser


t = '''
    Dr John Smith, M.D
2 Non-Important Street,
New York, Phone (000)-111-2222

Name: Marta Sharapova Date: 5/11/2022

Address: 9 tennis court, new Russia, DC

K

Prednisone 20 mg
Lialda 2.4 gram

Directions:

Prednisone, Taper 5 mig every 3 days,
Finish in 2.5 weeks a
Lialda - take 2 pill everyday for 1 month

Refill: 2 times
    
    '''
    
def test_get_name():
    p = PrescriptionParser(t)
    assert p.parse()['patient_name'] == 'Marta Sharapova'
    
# def test_get_name():
#     p = PrescriptionParser(t)
#     assert p.parse()['patient_name'] == 'Marta Sharapov'

def test_record_M():
    record_M =  PrescriptionParser(t).parse() 
    assert record_M == {'patient_name': 'Marta Sharapova', 'patient_address': '9 tennis court, new Russia, DC', 'patient_medicine': 'K\n\nPrednisone 20 mg\nLialda 2.4 gram', 'patient_directions': 'Prednisone, Taper 5 mig every 3 days,\nFinish in 2.5 weeks a\nLialda - take 2 pill everyday for 1 month', 'patient_refill': '2'}

    
    
    