import pydicom
from datetime import datetime

from docxtpl import InlineImage
import json
import numpy as np
from docxtpl import DocxTemplate

import dicomreader

def validate_region_number(region_number):
    valid_region_numbers = [
        '11', '12', '13', '14', '15', '16', '17', '18',
        '21', '22', '23', '24', '25', '26', '27', '28',
        '31', '32', '33', '34', '35', '36', '37', '38', 
        '41', '42', '43', '44', '45', '46', '47', '48'
    ]
    return region_number in valid_region_numbers

def get_quadrant_and_region(region_number):
    quadrant = int((int(region_number) - 1) / 8) + 1
    region_names = {
        '11': 'Upper right third molar',
        '12': 'Upper right second molar',
        '13': 'Upper right first molar',
        '14': 'Upper right second premolar',
        '15': 'Upper right first premolar',
        '16': 'Upper right canine',
        '17': 'Upper right lateral incisor',
        '18': 'Upper right central incisor',
        '31': 'Lower left third molar',
        '32': 'Lower left second molar',
        '33': 'Lower left first molar',
        '34': 'Lower left second premolar',
        '35': 'Lower left first premolar',
        '36': 'Lower left canine',
        '37': 'Lower left lateral incisor',
        '38': 'Lower left central incisor',
        '41': 'Lower right central incisor',
        '42': 'Lower right lateral incisor',
        '43': 'Lower right canine',
        '44': 'Lower right first premolar',
        '45': 'Lower right second premolar',
        '46': 'Lower right first molar',
        '47': 'Lower right second molar',
        '48': 'Lower right third molar',
    }
    region_name = region_names.get(region_number, 'Null')
    return quadrant, region_name

def get_dcm_attriutes(folder,):
    dcm_file = dicomreader.get_dicom_file(folder)
    json_file = 'middle.json'  

    with open(json_file) as f:
        json_data = json.load(f)

    attribute_tags = json_data['content']
    attributes = dicomreader.read_dcm_attributes(dcm_file, attribute_tags)
    ds = pydicom.read_file(dcm_file)
    return ds, attributes

def find_patient_age(dob):
    if len(dob) != 8:
        return "Invalid date format"
    year = int(dob[:4])
    month = int(dob[4:6])
    day = int(dob[6:])
    today = datetime.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

slice_mapping = {
    18: 9,
    17: 9,
    16: 9,
    15: 5,
    14: 5,
    13: 5,
    12: 4,
    11: 4,
    21: 4,
    22: 4,
    23: 5,
    24: 5,
    25: 5,
    26: 9,
    27: 9,
    28: 9,
}

def get_slice_count(region_number):
    if region_number in slice_mapping:
        return slice_mapping[region_number]
    else:
        return 0  

def calculate_slices(region_number):
    if region_number in slice_mapping:
        starting_index = 1 
        ending_index = 0 
        for region in slice_mapping:
            if region == region_number:
                ending_index = starting_index + get_slice_count(region_number) - 1
                break
            else:
                starting_index += get_slice_count(region)
        print(starting_index,ending_index)
        return starting_index, ending_index
    else:
        return None 

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def render_save_report(attributes, report_filepath):
    template_file = 'report_template.docx'  
    template = DocxTemplate(template_file)
    to_fill_in = {'img1': 'result.jpg', 'img2': 'result.jpg','img_pan':'panaroma.jpg'}
    for key, value in to_fill_in.items():
        image = InlineImage(template, value)
        attributes[key] = image
    template.render(attributes) 
    template.save(report_filepath)
