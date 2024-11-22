import re
from datetime import datetime
import os

from question_and_answer_api import ask_qa,api_schema
import json
# from database_connection import insertGondaExtractions,fetching_invoice_number
from database_utils import insertGondaExtractions,fetching_invoice_number

                

def type1(data):
    main_des = []
    line_items = []
    headers_skipped = False
    for line in data:
        if not headers_skipped:
            if 'DESCRIPTION' in line or 'AMOUNT' in line:
                headers_skipped = True
            continue

        table1 = line.split('|')[1:-1]
        # print(table1,">>>>",len(table1))


        if len(table1) == 5:
            if 'rate' in table1[0].lower() or 'rupees' in table1[0].lower():
                continue

            if re.search(r'(?si)rs\.[0-9,.]+',table1[0]):
                continue
                

            merge_column_data = table1[0].strip() +' '+ table1[1].strip()+' ' +table1[2].strip()+' '+table1[3].strip()
            # print(merge_column_data,">>>>>>>>>>>>?")
            
            line_item = {
                'description': merge_column_data,
                'quantity': '',
                'unit': '',
                'rate': '',
                'amount': table1[-1].strip().replace('Rs.',"")
            }

            line_items.append(line_item)

    return main_des,line_items


def aws_pretty_text(output_folder,text):

    for file in os.listdir(output_folder):
        if file.endswith('pretty.txt'):
            with open(os.path.join(output_folder, file), 'r', encoding="utf-8") as raw_data:
                data = raw_data.readlines()
            data2 = ' '.join(data)
            # print(data2,">>>")
            if ('DESCRIPTION' in data2 and 'AMOUNT' in data2):
                print('condition 1')
                a = type1(data)
                return a
           


# def vivek_sharma_association(file_name,text,res_para,output_folder,db_conn):
def neelam_thadani_invoice(file_name, text, res_para, output_folder, db_conn,category ,excel_id):
    # print(text,'\n\n')
    print("--------------","proforma format")
    
    time_stamp = datetime.now()


    
   

    schema, prompt = api_schema()
    result = ask_qa(text,prompt,schema)   ### QNA API.....

    print('result :',result,"\n\n")
    # try:
    #     result = json.loads(result)
    # except:
    #     result = ''
        
    # if result == '504.0 GatewayTimeout':
    #     result = ask_qa(text,prompt,schema)

    # if result["buyerName"] == '' or  result["buyerAddress"] == '' or result['vendorName'] == '' or result['vendorAddress'] == '':
    #     result = ask_qa(text,prompt,schema)
    
    # if result["buyerName"] == None or  result["buyerAddress"] == None or result['vendorName'] == None or result['vendorAddress'] == None:
    #     result = ask_qa(text,prompt,schema)
        
    if result == {}:
        result = ask_qa(text,prompt,schema)

    print('result :-',result)

    try:
        buyer_name = result["buyerName"]
    except:
        buyer_name = ''
    # print('buyer name :-',buyer_name,"\n\n")
    try:
        buyer_address = result["buyerAddress"]
    except:
        buyer_address = ''
    # print('buyer address :-',buyer_address,"\n\n")

    try:
        seller_name = result['vendorName']
    except:
        seller_name = ''
    # print('seller name :-',seller_name,"\n\n")

    try:
        seller_address = result['vendorAddress']
    except:
        seller_address = ''
    # print('seller address :-',seller_address,"\n\n")
    
    try:
        invoice_number = result['invoice_number']
    except:
        invoice_number = ''

    # print('invoice number :',invoice_number,'\n\n')
    
    try:
        invoice_date = result['invoice_date']
    except:
        invoice_date = ''
    # print('invoice date :',invoice_date,'\n\n')

    if invoice_number !="":
        check_invoice_status = fetching_invoice_number(db_conn,invoice_number)
        # print('check_invoice_status :',check_invoice_status,'\n\n')
        if check_invoice_status == None:
            # print('error in database')
            return 
        
        if check_invoice_status:
            # print('this invoice already present in database,duplicate invoice')
            return 'already present'
    else:
        pass

    
    buyer_pan = ''
    # print('buyer_pan :',buyer_pan,'\n\n')

    buyer_tin = ''
    # print('buyer_tin :',buyer_tin,'\n\n')

    
    buyer_service_tax_no = ''
    # print('buyer_service_tax_no :',buyer_service_tax_no,'\n\n')

    buyer_cst = '' 
    # print('buyer_cst :',buyer_cst,'\n\n')


    seller_pan = ''
    # print('seller_pan :',seller_pan,'\n\n')

    seller_tin = ''
    # print('seller_tin :',seller_tin,'\n\n')

    seller_service_tax = ''
    # print('seller_service_tax :',seller_service_tax,'\n\n')

    seller_cst = ''
    # print('seller_cst :',seller_cst,'\n\n')



    ######### To find Substation Name / Net Value / Less Retention........
    
    


    supply_civil_service = ''
    # print('supply_civil_service :',supply_civil_service,'\n\n')

    

    pkg_value =''
    # print("pkg value :",pkg_value,'\n\n')

    vat_gst = ''
    # print('vat_gst :',vat_gst,'\n\n')

    
    service_tax = ''
    # print('servive tax :',service_tax,'\n\n')

    
    gross_value = ''
    # print('gross_value :',gross_value,'\n\n')

    retention = ''
    # print('retention :',retention,'\n\n')

    advance_value = ''
    # print('advance_value :',advance_value,'\n\n')

    net_value = ''
    net_value = re.search(r'(?si)net\stotal.*?make\sall',text).group().replace('Rs.',"")
    net_value = re.findall(r'(?si)[0-9,.]+',net_value)[-1]
    # print('net_value :',net_value,'\n\n')
    

    vat = ''
    education_cess = ''
    he_education_cess = ''

    ### for line item 
    main_des,line_items = aws_pretty_text(output_folder,text)

    # print('main_des :',main_des,'\n\n')
    # print('line_items :',line_items,'\n\n')

    if main_des == [] and line_items == []:
        return 'error'

    for index,line_item in enumerate(line_items):

        des     = line_item['description']
        qty     = line_item['quantity'].strip()
        unit    = line_item['unit'].strip()
        rate    = line_item['rate'].strip()
        amount  = line_item['amount'].strip()

        file_name = file_name.split('\\')[-1]

        if index == 0 :
            data= (buyer_name,buyer_address,buyer_pan,buyer_tin,buyer_service_tax_no,buyer_cst,seller_name,seller_address,seller_pan,seller_tin,seller_service_tax,seller_cst,invoice_number,invoice_date,pkg_value,supply_civil_service,des,unit,qty,rate,amount,vat_gst,vat,service_tax,education_cess,he_education_cess,gross_value,advance_value,retention,net_value,file_name,time_stamp,category)
            print(data,len(data))
            insertGondaExtractions(db_conn,data)
            continue


        data= (buyer_name,buyer_address,buyer_pan,buyer_tin,buyer_service_tax_no,buyer_cst,seller_name,seller_address,seller_pan,seller_tin,seller_service_tax,seller_cst,invoice_number,invoice_date,pkg_value,supply_civil_service,des,unit,qty,rate,amount,'','','','','','','','','',file_name,time_stamp,category)
        print(data,len(data))
        insertGondaExtractions(db_conn,data)

        # print("-----------------------------------------------------------")

    return 'success'