import pydicom
import os

def get_dicom_file(folder_path):
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith('.dcm'):
                dcm_filepath = os.path.join(root, filename)
                return dcm_filepath
    return None


def read_dcm_attributes(dcm_file, attribute_tags):
    ds = pydicom.dcmread(dcm_file)
    attributes = {}
    for param in attribute_tags:
        attributes[param['name']] = ds[param['name']].value
    return attributes


def get_patient_id_from_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith('.dcm'):
                file_path = os.path.join(root, filename)
                dataset = pydicom.dcmread(file_path)
                patient_id = dataset.get('PatientID', 'Null')
                return patient_id
    return("Null")

def get_patinet_name(ds):
    id = ds.get('PatientID', 'Null')
    name = ds.get('PatientName', id)
    return str(name)[0:6]
