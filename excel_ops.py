import os
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
import re

from general_function import fileCleaner
from rules import page_number_match_rules

from database_utils import insertDataFileDetails

from pdf_ops import findAndSplitPdf




"""
The function `overrideHeaderName` updates the header names in the first row of an Excel
file.
"""
def overrideHeaderName(excel_file_path):
    wb = load_workbook(excel_file_path)
    sheet = wb['Sheet1']

    sheet['A1'] = 'DocumentName'
    sheet['B1'] = 'PageNumber'
    sheet['C1'] = 'IndexingName'

    wb.save(excel_file_path)


"""
The function `checkKeywordsAreAbsent` checks if any of the specified keywords are present in a
DataFrame and returns True if none are found.
"""
def checkKeywordsAreAbsent(dataFrame, keyword_pattern):
    return not any(dataFrame.applymap(lambda x: bool(keyword_pattern.search(x)) if isinstance(x, str) else False).any())



"""
The function `getPdfInfoByExcel` reads data from an Excel file, checks for specific keywords,
filters the data based on the keywords, and returns a list of PDF names and page numbers.

"""
def getInfoFromExcel(db_conn, execution_id, excel_file_path):
    keywords = ('invoice','invoices')
    # keywords = ('invocie',)
    # keywords = ('sale invoice','tax invoice')
    keyword_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b', re.IGNORECASE)

    excelFileName = os.path.basename(excel_file_path)
    dataFrame = pd.read_excel(excel_file_path)   
    dataFrame = dataFrame.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    # print(dataFrame,">>>>1")

    # Check keywords present or absent
    if checkKeywordsAreAbsent(dataFrame, keyword_pattern):
        split_pdf = 'no'
        table_status = 'fail'
        time_stamp = datetime.now()
        remark = 'keywords not found'
        print('remark :-',remark)
        data = (execution_id, excelFileName, '', '', '', split_pdf, table_status, time_stamp,remark)
        insertDataFileDetails(db_conn, data)
        return None

    # Filter DataFrame to include only rows where 'IndexingName' matches the keyword pattern
    dataFrame = dataFrame[dataFrame['IndexingName'].apply(lambda x: bool(keyword_pattern.search(str(x))))]
    # print(dataFrame,">>>>")
    pdf_name_list = dataFrame['DocumentName'].tolist()
    page_number_list = dataFrame['PageNumber'].tolist()
    indexing_name_list = dataFrame['IndexingName'].tolist()
    print("<<<", page_number_list, len(page_number_list))



    try:
        # page_number_list = [page_number_match_rules(str(i.replace(' ',""))) for i in page_number_list]
        page_number_list = [
            page_number_match_rules(str(i).replace(' ', '').replace('to', '-')) if isinstance(i, str) 
            else page_number_match_rules(str(i)) 
            for i in page_number_list
        ]
        page_number_list = [j for i in page_number_list for j in i]
        indexing_name_list = [i for i in indexing_name_list]
    except Exception as e:
        ## failed to identify page num using rule matching db insert
        pdf_name_list = []
        page_number_list = []
        split_pdf = 'no'
        table_status = 'fail'
        time_stamp = datetime.now()
        remark = 'rules not matched for page number - '
        print('remark :-',remark)
        data = (execution_id, excelFileName, '', '', '', split_pdf, table_status, time_stamp,str(remark))
        insertDataFileDetails(db_conn, data)
        print(f'Exception rule:- {e}')
        return None
    
    data = (pdf_name_list, page_number_list, indexing_name_list)
    
    return data



def getPDFdetails(config, db_conn, execution_id, excel_file_path): 

    # Override header from Excel
    overrideHeaderName(excel_file_path)     #renameHeaders

    # Get information for PDF processing
    pdf_info = getInfoFromExcel(db_conn, execution_id, excel_file_path)    #getInfoFromExcel

    if not pdf_info:
        return None
    
    if not findAndSplitPdf(config, db_conn, execution_id, pdf_info, excel_file_path):
        return None

    return True


