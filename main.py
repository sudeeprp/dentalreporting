import os
import mainuiprompts
import imageprocess
import imageannotate
import dentalreport
import mainuiprompts
import dicomreader
from docxtpl import DocxTemplate

while True:
    selected_folder = mainuiprompts.prompt_patient_folder()
    ds, attributes = dentalreport.get_dcm_attriutes(selected_folder)
    
    pixel_spacing = ds.get('PixelSpacing', 'Null')
    pixels = int(pixel_spacing[1] * 1000)
    
    print("\nPlease enter following details:")
    region_number = mainuiprompts.prompt_region_number()

    quadrant, region_name = dentalreport.get_quadrant_and_region(region_number)
    print(f"\nThe selected tooth is in the Quadrant: {quadrant} Region: {region_name}")

    num_of_implants = mainuiprompts.prompt_num_of_implants()

    attributes['RegionName'] = region_name
    attributes['date_now'] = dentalreport.get_current_date()
    attributes['PatientAge'] = dentalreport.find_patient_age(attributes['PatientBirthDate'])
    attributes['PixelSpacing'] = pixels 

    mapping = dentalreport.allocate_indices(region_number)
    attributes = dentalreport.begin_end_mapping(attributes,mapping)

    confirm = input("\nContinue to generate a pre-filled report? (yes/no): ").lower()
    if confirm == 'no' or confirm == 'n':
        print("No report will be generated. Thank you.")
    else:
        
        windowed_pixel_array = imageprocess.get_windowed_pixels(ds)

        image = imageprocess.convert_pixel_to_image(windowed_pixel_array)

        image = imageannotate.annotate(ds, image)

        image.save("result.jpg")
        
        images = imageprocess.find_panoramic_view_image(selected_folder)

        images.save("panaroma.jpg")

        images = imageprocess.find_panoramic_view_image(selected_folder)

        images.save("panaroma.jpg")

        template_file = 'report_template.docx' 
         
        filename = dicomreader.get_patinet_name(ds)
        report_filename = f"{filename}_{dentalreport.get_current_datetime()}.docx"
        report_filepath = os.path.join(selected_folder, report_filename)
        
        template = DocxTemplate(template_file)
        attributes = dentalreport.addvirtual_implant_save(attributes,num_of_implants,template)
        
        dentalreport.render_save_report(template,attributes, report_filename)

        
        
        print("\nSuccessfully generated report!!")
        print("\tAt:", selected_folder)
        print("\tAs:", report_filename)
        print()
    