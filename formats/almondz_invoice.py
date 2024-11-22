import os
from datetime import datetime
from question_and_answer_api import ask_qa,api_schema
import json
# from database_connection import insertGondaExtractions,fetching_invoice_number
from database_utils import insertGondaExtractions,fetching_invoice_number
from general_function import get_num
import re


def type1(data):
    main_des = []
    line_items = []
    headers_skipped = False
    for line in data:
        # print(line,">>>>>")
        if not headers_skipped:
            if 'PARTICULARS' in line or 'AMOUNT' in line:
                headers_skipped = True
            continue


        table1 = line.split('|')[1:-1]
        print(table1,"???",len(table1))
        
    
        if len(table1) == 2:

            if 'Total' in table1[0].strip():
                break

            line_item = {
                'description': table1[0].strip(),
                'quantity': '',
                'unit': '',
                'rate': '',
                'amount': table1[-1].strip()
            }

            line_items.append(line_item)

    return main_des,line_items



def pretty_text_data(output_folder):

    for file in os.listdir(output_folder):
        if file.endswith('pretty.txt'):
            # print(file)
            with open(os.path.join(output_folder, file), 'r', encoding="utf-8") as raw_data:
                data = raw_data.readlines()
                data2 = ' '.join(data)
                # print(data2,'\n')
                if ('PARTICULARS' in data2 and 'AMOUNT' in data2):
                    print('condition 1')
                    a = type1(data)
                    return a
                



def almondz_invoice(file_name,text,res_para,output_folder,db_conn,category,excel_id):

    print('------------- almondz invoice')
  
    schema, prompt = api_schema()

    # print(text,"\n\n")
    result = ask_qa(text,prompt,schema)   ### QNA API.....

    # try:
    #     result = json.loads(result)
    # except:
    #     result = ''
    # print('result :-',result)

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
    # print('buyer name :',buyer_name,'\n\n')

    try:
        buyer_address = result["buyerAddress"]
    except:
        buyer_address = ''
    # print('buyer address :',buyer_address,'\n\n')

    try:
        seller_name = result['vendorName']
    except:
        seller_name = ''
    # print('seller name :',seller_name,'\n\n')

    try:
        
        seller_address = ''
    except:
        seller_address = ''
    # print('seller address :',seller_address,'\n\n')

    try:
        invoice_number = result['invoice_number']
    except:
        invoice_number = ''
    # print('invoice_number :',invoice_number,'\n\n')

    try:
        invoice_date = result['invoice_date']
    except:
        invoice_date = ''
    # print('invoice_date :',invoice_date,'\n\n')

    check_invoice_status = fetching_invoice_number(db_conn,invoice_number)
    # print('check_invoice_status :',check_invoice_status)
    if check_invoice_status == None:
        # print('error in database')
        return 
    
    if check_invoice_status:
        # print('this invoice already present in database,duplicate invoice')
        return 'already present'
    
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

    pkg_value = ''
    # print("pkg value :",pkg_value,'\n\n')


    supply_civil_service = ''
    # print('supply_civil_service :',supply_civil_service,'\n\n')
    
    
    retention = ''
    # print('retention :',retention,'\n\n')
    
    advance_value = ''
    # print('advance_value :',advance_value,'\n\n')

    gross_value = ''
    if re.search(r'(?si)total.*?add\:\sservice\stax',text):
        gross_value = re.search(r'(?si)total.*?add\:\sservice\stax',text).group()
        gross_value = re.findall(r'[0-9,.]+',gross_value)[-1]
    else:
        gross_value = ''
    # print('gross_value :',gross_value,'\n\n')
    
    
    
    if re.search(r'(?si)add\:\sservice\stax.*?add\:\seducation\scess',text):
        service_tax_gst = re.search(r'(?si)add\:\sservice\stax.*?add\:\seducation\scess',text).group()
        service_tax_gst = re.findall(r'[0-9,.]+',service_tax_gst)[-1]
    else:
        service_tax_gst = ''
    # print('service_tax_gst :',service_tax_gst,'\n\n')

    if re.search(r'(?si)add\:\seducation\scess.*?add:\ssecondary\sand\shigher\seducation\scess',text):
        education_cess = re.search(r'(?si)add\:\seducation\scess.*?add:\ssecondary\sand\shigher\seducation\scess',text).group()
        education_cess = re.findall(r'[0-9,.]+',education_cess)[-1]
    else:
        education_cess = ''

    # print('education cess:',education_cess,'\n\n')

    if re.search(r'(?si)add:\ssecondary\sand\shigher\seducation\scess.*?amount',text):
        sh_education_cess = re.search(r'(?si)add:\ssecondary\sand\shigher\seducation\scess.*?amount',text).group()
        sh_education_cess = re.findall(r'[0-9,.]+',sh_education_cess)[-1]
    else:
        sh_education_cess = ''
    # print('sh education cess :',sh_education_cess,'\n\n')

    if re.search(r'(?si)amount\sin\swords.*?for\salmondz',text):
        net_value = re.search(r'(?si)amount\sin\swords.*?for\salmondz',text).group()
        net_value = re.findall(r'[0-9,.]+',net_value)
        net_value = get_num(net_value)
    else:
        net_value = ''
        
    # print('net value :',net_value,'\n\n')

    vat_gst = ''
    vat = ''

    file_name = file_name.split('\\')[-1]


    main_des,line_itmes = pretty_text_data(output_folder)
    # print('main_des :',main_des)
    # print('line_itmes :',line_itmes,'\n\n')


    for index,line_item in enumerate(line_itmes):
        # print(line_item,">>>",index)
        if main_des == []:
            des = line_item['description']
        if main_des != []:
            des = str(main_des[0].strip()) + " " + str(line_item['description'])

        des = des.replace(pkg_value.strip(),"")
            
        
        qty = line_item['quantity']
        unit = line_item['unit']
        rate = line_item['rate']
        amount = line_item['amount']
        timestamp = datetime.now()

        if index == 0:
            
            data= (buyer_name,buyer_address,buyer_pan,buyer_tin,buyer_service_tax_no,buyer_cst,seller_name,seller_address,seller_pan,seller_tin,seller_service_tax,seller_cst,invoice_number,invoice_date,pkg_value.strip(),supply_civil_service,des,unit,qty,rate,amount,vat_gst,vat,service_tax_gst,education_cess,sh_education_cess,gross_value,advance_value,retention,net_value,file_name,timestamp,category)
            print(1,data,len(data))
            insertGondaExtractions(db_conn,data)
            continue

        
        
        data= (buyer_name,buyer_address,buyer_pan,buyer_tin,buyer_service_tax_no,buyer_cst,seller_name,seller_address,seller_pan,seller_tin,seller_service_tax,seller_cst,invoice_number,invoice_date,pkg_value.strip(),supply_civil_service,des,unit,qty,rate,amount,'','','','','','','','','',file_name,timestamp,category)
        print(data,len(data))

        insertGondaExtractions(db_conn,data)
    
    return 'success'


    

