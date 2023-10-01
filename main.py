import os
import mainuiprompts
import imageprocess
import imageannotate
import dentalreport
import mainuiprompts
import dicomreader

while True:
    selected_folder = mainuiprompts.prompt_patient_folder()
    ds, attributes = dentalreport.get_dcm_attriutes(selected_folder)

    print("\nPlease enter following details:")
    region_number = mainuiprompts.prompt_region_number()

    quadrant, region_name = dentalreport.get_quadrant_and_region(region_number)
    print(f"\nThe selected tooth is in the Quadrant: {quadrant} Region: {region_name}")

    attributes['date_now'] = dentalreport.get_current_date()
    attributes['PatientAge'] = dentalreport.find_patient_age(attributes['PatientBirthDate'])

    mapping = dentalreport.allocate_indices(region_number)
    print(mapping)
    attributes = dentalreport.begin_end_mapping(attributes,mapping)
    print(attributes)

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

        filename = dicomreader.get_patinet_name(ds)
        report_filename = f"{filename}_{dentalreport.get_current_datetime()}.docx"
        report_filepath = os.path.join(selected_folder, report_filename)
        dentalreport.render_save_report(attributes, report_filepath)

        print("\nSuccessfully generated report!!")
        print("\tAt:", selected_folder)
        print("\tAs:", report_filename)
        print()
