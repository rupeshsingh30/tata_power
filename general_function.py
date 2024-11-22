
import os
import shutil


def fileCleaner(folder_path):

    try:
        for folder in folder_path:
            for file in os.listdir(folder):
                filepath = os.path.join(folder,file)
                os.remove(filepath)
    except:
        pass

    

"""
The function checks if there are no files with specified extensions in a given directory.
"""
def hasNoExcelFiles(excel_dir):
    extensions = ('.xls', '.xlsx')
    if any(file.endswith(extensions) for file in os.listdir(excel_dir)):
        return False  # Excel files are found
    
    return True  # No Excel files found








def copy_folders_to_destination(config, destination_folder_name):
    # Extract folder paths from the config
    worked_folder    = config['file_dir']['worked_folder']
    duplicate_folder = config['file_dir']['duplicate_folder']
    new_formats      = config['file_dir']['new_formats']
    error_folder     = config['file_dir']['error_folder']

    box_path         = config['file_dir']['error_folder']

    source_folders = [worked_folder, duplicate_folder, new_formats, error_folder]  
    destination_folder = os.path.join(r'D:\tata_power_gonda\gonda_process\box', destination_folder_name)

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Copy each folder to the destination folder
    for folder in source_folders:
        if os.path.exists(folder):
            shutil.copytree(folder, os.path.join(destination_folder, os.path.basename(folder)))
        else:
            print(f"Folder {folder} does not exist.")



import re

def get_num(val):
    for v in val[::-1]:
        if re.search(r'[0-9]+',v):
            return v
