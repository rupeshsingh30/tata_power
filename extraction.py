import shutil
import os
import re
from datetime import datetime
from aws_trigger import trigger
from formats.sale_invoices import sale_invoice
from formats.tax_invoices import tax_invoice
from formats.tax_invoices_p import tax_invoice_p
from formats.associates_viveksharma import vivek_sharma_association
from formats.associates_ss_sharma import ss_sharma_association
from formats.proforma_invoice import proforma_invoice
from formats.neelam_thadani_invoice import neelam_thadani_invoice
from formats.vinayak_hr_solutioin import vinayak_hr_solution
from formats.reatil_invoice import retail_invoice
from formats.almondz_invoice import almondz_invoice
from formats.charan_gupta_consultant import charan_gupta_consultant
from database_utils import insertGondaExtractions,insertGondaExtractionError

import warnings
warnings.filterwarnings('ignore')

def moveFile(original_path, error_folder):
    shutil.move(original_path, error_folder)

def removeSpaceFromFileName(file_folder):
    for input_path in file_folder: 
        if " " in input_path:
            old_path = input_path
            file_name = os.path.basename(input_path).replace(" ","_").replace(",","_").replace("'","_")
            new_path = os.path.join(os.path.dirname(old_path), file_name)
            os.rename(old_path, new_path)

def checkIfPdfFormatIsNew(text):
    header_text = ''

    if re.search(r'(?si).*?(triplicate|triplicat)', text):
        header_text = re.search(r'(?si).*?(triplicate|triplicat)', text).group()
    elif re.search(r'(?si).*?(invoice\sno)', text):
        header_text = re.search(r'(?si).*?(invoice\sno)', text).group()
    elif re.search(r'(?si).*?(proforma\sto)', text):
        header_text = re.search(r'(?si).*?(proforma\sto)', text).group()
    elif re.search(r'(?si).*?date',text):
        header_text = re.search(r'(?si).*?date',text).group()
    
    return header_text

def checkInvoiceCategory(text, header_text, pdf_file_path, new_formats,error_folder):
    expected_buyer = [
        'South East UP Power Transmission Co. Ltd.', 
        'South East UP Power Transmission Co LTD', 
        'south east up power transmission co ltd',
        'uth East UP Power Transmission Co. Ltd.', 
        'East UP Power Transmission Co. Ltd',
        'east up power transmission co. ltd',
        'SOUTH EAST U.P. POWER TRANSMISSION COMPANY',
        'south east u.p. power transmission company',
        'South East U.P. Power Transmission Company',
        'South East U.P Power Transmission',
        'south east u.p power transmission',
        'SOUTH EAST U.P. POWER TRANSMISSION',
        'SOUTH EAST UP POWER TRANSMISSION CO LTD',
        'South East Up Power Transmission Co.Ltd',
        'south east up power transmission co.ltd',
        'SOUTH EAST U.P POWER TRANSMISSION',
        'SOUTH EAST U. P POWER TRANSMISSION',
        'South East UP Power Transmission Company Limited',
        'south east up power transmission company limited',
        'SOUTH EAST U. P. POWER TRANSMISSION COMPANY',
        'south east u. p. power transmission company'
        'SOUTH EAST U. P. POWER TRANSMISSION COMPANY LIMITED',
        'south east u. p. power transmission company limited',
        'South East UP Power Transmission Private Limited',
        'south east up power transmission private limited',
        'South East 1.P. Power Transmission Company Limited',
        'South East UP Power Transmission Co. Ltd.'
    ]

    expected_vendor = [
        'ICI - C&C MAINPURI JV',
        'ICI-C&C MAINPURI -JV',
        'ICI - C&C MAINPURI -JV',
        'ICI C&CMAINPURI -JV',
        'ICI - C&CMAINPURI -JV',
        'ICI C&C MAINPURI-JV',
        'ICI-C&C MAINPURI - JV',
        'ICI-C&CMAINPURI -JV',
        'ICI C&CMAINPURI JV',
        'Isolux Corsan India Engineering',
        'ISOLUX CORSAN INDIA ENGINEERING',
        'ISOLUX CORSAN POWER CONCESSIONS INDIA'
    ]
    if 'sale invoice' in header_text.lower() and any(substring in text.lower() for substring in expected_buyer) and any(substring in text for substring in expected_vendor):
        return 'sale invoice'
    elif 'tax invoice(p)' in header_text.lower() and any(substring in text.lower() for substring in expected_buyer):
        return 'tax invoice(p)'
    elif 'tax invoice' in header_text.lower() and 'Person' in text  and  any(substring in text for substring in expected_buyer):
        return 'tax invoice(p)'
    elif 'tax invoice' in header_text.lower() and any(substring in text.lower() for substring in expected_buyer) and any(substring in text for substring in expected_vendor):
        return 'tax invoice'
    elif 'vivek sharma' in header_text.lower() and any(substring in text.lower() for substring in expected_buyer):
        return 'vivek sharma associates'
    elif 's.s.sharma & associates' in header_text.lower() and any(substring in text.lower() for substring in expected_buyer):
        return 's.s.sharma & associates'
    elif 'proforma invoice' in header_text.lower() and any(substring in text.lower() for substring in expected_buyer):
        return 'proforma invoice'
    elif 'neelam thadani' in header_text.lower() and any(substring in text.lower() for substring in expected_buyer):
        return 'neelam thadani invoice'
    elif 'vinayak hr solutions pvt ltd' in header_text.lower() and any(substring in text.lower() for substring in expected_buyer):
        return 'vinayak hr solution pvt ltd'
    elif 'retail invoice' in header_text.lower() and any(substring in text.lower() for substring in expected_buyer):
        return 'retail invoice'
    elif 'almondz' in header_text.lower() and any(substring in text for substring in expected_buyer):
        return 'almondz'
    elif 'charan gupta consultants' in header_text.lower() and any(substring in text for substring in expected_buyer):
        return 'chatan gupta consultants'
    else:
        return None

def extractInvoiceInfo(pdf_file_path, text, res_para, output_folder, db_conn, excel_id, category):
    func_mapping = {
        "sale invoice"          : sale_invoice,
        "tax invoice(p)"        : tax_invoice_p,
        "tax invoice"           : tax_invoice,
        "vivek sharma associates": vivek_sharma_association,
        "s.s.sharma & associates": ss_sharma_association,
        "proforma invoice"      : proforma_invoice,
        "neelam thadani invoice": neelam_thadani_invoice,
        'vinayak hr solution pvt ltd': vinayak_hr_solution,
        'retail invoice'        : retail_invoice,
        'almondz'               : almondz_invoice,
        'chatan gupta consultants' : charan_gupta_consultant

    }
    invoice_func = func_mapping[category]
    return invoice_func(pdf_file_path,text,res_para,output_folder,db_conn,category,excel_id)
    try:
        invoice_func = func_mapping[category]
        return invoice_func(pdf_file_path,text,res_para,output_folder,db_conn,category,excel_id)
    except Exception as e:
        print(f"Error in {category} function: ", str(e))
        return "error"

def extraction(config, db_conn, pdf_file_path, excel_id):
    temp_folder = config['file_dir']['temp_file']
    output_folder = config['file_dir']['output_folder']
    report_folder = config['file_dir']['report_path']

    worked_folder = config['file_dir']['worked_folder']
    duplicate_folder = config['file_dir']['duplicate_folder']
    new_formats = config['file_dir']['new_formats']
    error_folder = config['file_dir']['error_folder']

    in_reading_text, text = trigger(pdf_file_path, output_folder)
    text = ' '.join(text.split('\n'))
    print("Text:", text, '\n\n')
    
    status_folder_map = {
        'already present': duplicate_folder,
        'success': worked_folder,
        'error': error_folder
    }
    
    res_para = ''
    header_text = checkIfPdfFormatIsNew(text)
    print('Header Text:', header_text.lower())
    
    if header_text == '':
        print('New format detected')
        file_name = os.path.basename(pdf_file_path)

        insertGondaExtractionError(db_conn,excel_id,file_name,'new format')
        moveFile(pdf_file_path, new_formats)
        return None
    
    category = checkInvoiceCategory(text, header_text, pdf_file_path, new_formats,error_folder)
    print('Category:', category,"\n\n")
    
    if not category:
        print('Could not identify PDF category')
        file_name = os.path.basename(pdf_file_path)
        
        insertGondaExtractionError(db_conn, excel_id, file_name,'new format')
        moveFile(pdf_file_path, new_formats)

        return None
        
    status = extractInvoiceInfo(pdf_file_path, text, res_para, output_folder, db_conn, excel_id, category)
    print("Status:", status)

    if status == 'error':
        file_name = os.path.basename(pdf_file_path)
        timestamp = datetime.now()
        insertGondaExtractionError(db_conn,excel_id,file_name,'error')

    if status in status_folder_map:
        moveFile(pdf_file_path, status_folder_map[status])
    else:
        print(f"Unexpected status: {status}")


from database_utils import dbConnection
from config import loadConfig
from general_function import fileCleaner

config = loadConfig(r'D:\tata_power_gonda\gonda_process\code\app.config')
dbConn = dbConnection(config)

tempFolder = config['file_dir']['temp_file']
outputFolder = config['file_dir']['output_folder']
outputFolder = [outputFolder]

for file in os.listdir(tempFolder):
    pdfFilePath = os.path.join(tempFolder, file)
    # print(pdfFilePath,">>>>")
    
    fileCleaner(outputFolder)

    if not extraction(config, dbConn, pdfFilePath, excel_id=6):
        continue

