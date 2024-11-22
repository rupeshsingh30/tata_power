import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import PyPDF2

from rules import excel_pdf_name_rule
from database_utils import insertDataFileDetails

"""
The function `splitPdfFile` takes a PDF file path, a temporary directory path, and a list of page
numbers, then splits the PDF file into separate PDF files based on the specified page numbers.
"""
def splitPdfFile(pdf_path, temp_folder, page_numbers):
   
    # Check if the output path exists, create it if it doesn't
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # List to hold names of output files
    output_files = []
    status = True
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            filename = os.path.basename(pdf_path)

            for page_number in page_numbers:
                # Check if the page number is valid
                if page_number < 1 or page_number > num_pages:
                    print(f"Error: Page number {page_number} is out of range (1-{num_pages}) for file '{filename}'")
                    continue  # Skip to the next page number

                # Create a new PDF writer
                writer = PyPDF2.PdfWriter()
                writer.add_page(reader.pages[page_number - 1])

                # Construct the output PDF file path
                output_pdf = os.path.join(temp_folder, f"{os.path.splitext(filename)[0]}_page_{page_number}.pdf")
                
                # Write the new PDF to disk
                with open(output_pdf, 'wb') as new_file:
                    writer.write(new_file)

                output_files.append(output_pdf)       
    except Exception as e:
        print(f"Error: {e}")
        status = False
            
    return status

# splitPdfFile(r"D:\tata_power_gonda\gonda_process\file_dir\scan_pdf\761_to_762.pdf", r'D:\tata_power_gonda\gonda_process\file_dir\temp', [2,5,104,107])
"""
The function `findPdfs` takes an Excel basename and a directory path, iterates through PDF
basenames in the directory, and returns a list of PDF paths that match a specific rule.
"""
def findPdfs(excel_basename, pdf_dir):
    
    pdf_names = []
    for pdf_basename in os.listdir(pdf_dir):
        if excel_pdf_name_rule(excel_basename, pdf_basename):
            split_pdf_path = os.path.join(pdf_dir, pdf_basename)
            pdf_names.append(split_pdf_path)
            return pdf_names
                
    return None

"""
The function `findAndSplitPdf` returns a boolean value `True` if the process is
successful. If the process encounters any errors or failures during the identification or splitting
of PDFs, it will not return anything and will insert relevant details into the database.
"""
def findAndSplitPdf(config, db_conn,execution_id, pdf_info, excel_file_path):
    
    pdf_dir = config['file_dir']['scan_pdf_path']
    temp_folder = config['file_dir']['temp_file']
    excel_basename = os.path.basename(excel_file_path)
    

    pdf_name_list = pdf_info[0]
    page_number_list = pdf_info[1]
    
    pdf_names = findPdfs(excel_basename, pdf_dir)
    # pdf_names = None
    
    
    if not pdf_names:                                 # failed to identify pdf, insert in db
        remark = 'failed to identify pdfs name'
        print('remark :-',remark)
        timestamp = datetime.now()
        data = (execution_id, excel_basename, '', '', '', 'no', 'fail', timestamp, remark)
        insertDataFileDetails(db_conn, data)
        return None
    
    for pdf_file in pdf_names:
        pdf_file_path = os.path.join(pdf_dir, pdf_file)

        file_split_status = splitPdfFile(pdf_file_path,temp_folder, page_number_list)
        # file_split_status = None
        if not file_split_status:                      # failed to split pdf, insert in db 
            remark = 'failed to split pdf'
            print('remark :-',remark)
            split_pdf = 'no'
            status = 'fail'
            timestamp = datetime.now()
            pdf_basename = os.path.basename(pdf_file_path)
            data = (execution_id, excel_basename,'', ','.join(map(str, page_number_list)), pdf_basename, split_pdf, status, timestamp, remark)
            insertDataFileDetails(db_conn, data)
            return None
        
    ## successfully insert details into first table
    remark = ''
    split_pdf = 'yes'
    status = 'pass'
    timestamp = datetime.now()
    pdf_basename = os.path.basename(pdf_file_path)
    data = (execution_id, excel_basename, '', ','.join(map(str, page_number_list)), pdf_basename, split_pdf, status, timestamp, remark)
    insertDataFileDetails(db_conn, data)
    return True

