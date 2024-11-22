import os
from excel_ops import getPDFdetails
from general_function import hasNoExcelFiles, fileCleaner,copy_folders_to_destination
from database_utils import dbConnection,pullReport,getExcelId
from config import loadConfig
# from extraction import extraction

def main(config, db_conn):
    excel_path = config['file_dir']['excel_path']
    temp_folder = config['file_dir']['temp_file']
 
    output_folder = config['file_dir']['output_folder']
    report_folder = config['file_dir']['report_path']

    worked_folder    = config['file_dir']['worked_folder']
    duplicate_folder = config['file_dir']['duplicate_folder']
    new_formats      = config['file_dir']['new_formats']
    error_folder     = config['file_dir']['error_folder']

    remove_files_path = [temp_folder,output_folder,report_folder,worked_folder,duplicate_folder,new_formats,error_folder]

    if hasNoExcelFiles(excel_path):
        print('No Excel files in this directory')
        return None
    
    execution_id = 1000

    for file in os.listdir(excel_path):
        excel_file_path = os.path.join(excel_path, file)
        print(f'Processing file: {excel_file_path}')

        ### Clean the input folder before processing
        fileCleaner(remove_files_path)

        ### Process Excel and split PDF
        pdf_info = getPDFdetails(config, db_conn, execution_id, excel_file_path)  
        # split_status = True

        output_folder = [output_folder]


        ###get excel id form here 
        excel_id = getExcelId(db_conn)
        print(excel_id)

    #     if pdf_info:
    #         # Perform extraction on each PDF in the input folder
    #         for file in os.listdir(temp_folder):
    #             pdf_file_path = os.path.join(temp_folder,file)
                
    #             fileCleaner(output_folder)

    #             if not extraction(config,db_conn,pdf_file_path,excel_id):
    #                 continue

    #     else:
    #         print('Error during PDF splitting. Skipping to next file.')
        



    #     copy_folders_to_destination(config, os.path.basename(excel_file_path.replace('.xlsx',"")))
    # pullReport(report_folder,db_conn)
    return True

if __name__ == "__main__":
    config = loadConfig(r'D:\tata_power_gonda\gonda_process\code\app.config')
    db_conn = dbConnection(config)
    result = main(config, db_conn)
    print(result)




