import tkinter as tk
from tkinter import filedialog
import dicomreader
import dentalreport
from PIL import Image

def select_patient_folder():
    while True:
        confirm = input("\nSelect a patient folder? (yes/no): ").lower()
        if confirm == 'no' or confirm == 'n':
            print("Thank you for using Autofill Reports!!\n")
            exit()
        else:
            selected_folder = get_selected_folder()
            print("Selected Patient from:", selected_folder)
            return selected_folder

def get_selected_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path

def prompt_patient_folder():
    while True:
        selected_folder = select_patient_folder()
        patient_id = dicomreader.get_patient_id_from_folder(selected_folder)
        if patient_id == 'Null':
            print("Patient ID not found. Please select a different patient folder.")
        else:
            return selected_folder

def prompt_region_number():
    while True:
        region_number = input("Region number: ")
        if dentalreport.validate_region_number(region_number):
            return region_number
        else:
            print("Invalid region number. Please enter a valid FDI teeth number (11-48).")
            image_path = 'pic4.png'
            img = Image.open(image_path)
            img.show()

def prompt_num_of_implants():
    implants = input("Number of implants:")
    return int(implants)