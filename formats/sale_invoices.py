import os
from datetime import datetime
from question_and_answer_api import ask_qa,api_schema
import json
# from database_connection import insertGondaExtractions,fetching_invoice_number
from database_utils import insertGondaExtractions,fetching_invoice_number
from general_function import get_num

def type1(data):
    main_des = []
    line_items = []
    headers_skipped = False
    for line in data:
        # print(line,">>>>>")
        if not headers_skipped:
            if 'Description' in line or 'Quantity' in line or 'Qty' in line or 'Invoice Amount' in line:
                headers_skipped = True
            continue


        table1 = line.split('|')[1:-1]
        # print(table1,"???",len(table1))
        
        try:
            zero_postion = re.sub(r'(?si)note.*|ote: The.*|N. The above.*',"",table1[0])
            table1[0] = zero_postion
        except:
            pass
        
        if len(table1) == 5:

            if table1[0].strip() != '' and table1[1].strip() == '' and table1[2].strip() == '' and table1[3].strip() == '' and table1[4].strip() == '':
                main_des.append(table1[0])
                continue

            if table1[0].strip() == '':
                continue

            if 'Less Amount' in  table1[1] or 'Less' in table1[1]:
                continue
            
            if 'Gross Value' in table1[2] or 'Gross' in table1[2]:
                continue
            if 'Varified' in table1[0] or 'paint' in table1[0] or 'smith' in table1[0] or 'knot' in table1[0] or 'verified' in table1[0] or 'Less' in table1[0] or 'Add VAT @ 4%' in table1[0] or 'have' in table1[0] or 'The above sale' in table1[0] or 'fulary' in table1[0] or 'Auley' in table1[0] or 'Verit d' in table1[0]:
                continue
            if 'Less' in table1[3]:
                continue

            if table1[1].strip() == '' and table1[3].strip() =='' and table1[4].strip() == '':
                continue

            line_item = {
                'description': table1[0].strip(),
                'quantity': table1[2].strip(),
                'unit': table1[1].strip(),
                'rate': table1[3].strip(),
                'amount': table1[4].strip()
            }

            line_items.append(line_item)
        if len(table1) == 6:
            # print(6)

            if table1[0].strip() != '' and table1[1].strip() == '' and table1[2].strip() == '' and table1[3].strip() == '' and table1[4].strip() == '' and table1[5].strip() == '':
                main_des.append(table1[0])
                continue

            if table1[0].strip() == '':
                continue

            if 'Less Amount' in  table1[1] or 'Less' in table1[1]:
                continue
            
            if 'Gross Value' in table1[2] or 'Gross' in table1[2]:
                continue
            if 'Varified' in table1[0] or 'paint' in table1[0] or 'smith' in table1[0] or 'knot' in table1[0] or 'verified' in table1[0] or 'Less' in table1[0] or 'Add VAT @ 4%' in table1[0] or 'have' in table1[0] or 'The above sale' in table1[0] or 'fulary' in table1[0] or 'Auley' in table1[0] or 'Verit d' in table1[0]:
                continue
            if 'Less' in table1[3]:
                continue

            if table1[1].strip() == '' and table1[3].strip() =='' and table1[4].strip() == '':
                continue

            line_item = {
                'description': table1[0].strip(),
                'quantity': table1[2].strip(),
                'unit': table1[1].strip(),
                'rate': table1[3].strip(),
                'amount': table1[5].strip()
            }

            line_items.append(line_item)
   
            
        if len(table1) == 7:
            # print(7)

            try:
                zero_postion = re.sub(r'(?si)note.*|ote: The.*|N. The above.*',"",table1[1])
                table1[1] = zero_postion
            except:
                pass
            # print(table1)
            
            if table1[1].strip() != '' and table1[2].strip() == '' and table1[3].strip() == '' and table1[4].strip() == '' and table1[5].strip() == '':
                main_des.append(table1[1])
                continue

            if table1[0].strip() != '' and table1[1].strip() == '' and table1[2].strip() == '' and table1[3].strip() == '' and table1[4].strip() == '' and table1[5].strip() == '':
                main_des.append(table1[0])
                continue

            if 'Less Amount' in  table1[1] or 'Less' in table1[1]:
                continue

            if 'Less Amount' in table1[2] or 'Gross Value' in table1[2] or 'Net Value' in table1[2]:
                continue
            
            if 'Gross Value' in table1[3] or 'Net Value' in table1[3] or 'Less' in table1[3]:
                break
            # if '' in table1[2].strip() and '' in table1[3].strip() and '' in table1[4].strip() and '' in table1[5].strip() and '' in table1[6].strip():
            #     continue
            
            # if table1[2].strip() == '' and table1[3].strip() == '' and table1[4].strip() == '' and table1[5].strip() == '' and table1[6].strip() == '':
            #     print(10000)
            #     break

            if table1[0].strip() == '' and table1[6].strip() != '':
                line_item = {
                    'description': table1[1].strip(),
                    'unit': table1[2].strip(),
                    'quantity': table1[3].strip(),
                    'rate': table1[4].strip(),
                    'amount': table1[6].strip().replace(',', '')
                }


                line_items.append(line_item)

            if table1[0].strip() != '' and table1[4].strip() == '':
                line_item = {
                    'description': table1[0].strip(),
                    'unit': table1[1].strip(),
                    'quantity': table1[2].strip(),
                    'rate': table1[3].strip(),
                    'amount': table1[5].strip()
                }
                line_items.append(line_item)
            
            if table1[0].strip() != '' and table1[4].strip() != '':
                line_item = {
                    'description': table1[0].strip(),
                    'unit': table1[1].strip(),
                    'quantity': table1[2].strip(),
                    'rate': table1[3].strip(),
                    'amount': table1[4].strip()
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
                if ('Description' in data2 and 'Quantity' in data2 and 'Unit Rate' in data2 and 'Amount' in data2 and 'Invoice' in data2):
                    print('condition 1')
                    a = type1(data)
                    return a
                elif ('Description' in data2 and 'Quantity' in data2 and 'UMI Rate' in data2 and 'Amount' in data2 and 'Invoice' in data2):
                    print('condition 2')
                    a = type1(data)
                    return a
                


import re

def sale_invoice(file_name,text,res_para,output_folder,db_conn,category,excel_id):

  
    schema, prompt = api_schema()

    # print(text,"\n\n")
    result = ask_qa(text,prompt,schema)   ### QNA API.....
    # result = ask_qa(res_para,prompt,schema)   ### QNA API.....
    try:
        result = json.loads(result)
    except:
        result = ''
    
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
        # buyer_name = result["buyerName"]
        buyer_name = 'South East UP Power Transmission Co. Ltd.'
    except:
        buyer_name = ''
    
    try:
        # buyer_address = result["buyerAddress"]
        buyer_address = '601,602, Shalimar Titanium, 6th Floor, Plot No. TC G 1/1, Near Gandhi Pratiishthan, Vibhuti Khand, Gomti Nagar, Lucknow.'
    except:
        buyer_address = ''

    try:
        seller_name = result['vendorName']
    except:
        seller_name = ''

    try:
        
        seller_address = result['buyerAddress']
        seller_address = buyer_address
    except:
        seller_address = ''


    invoice_number = re.search(r'(?si)invoice\sno.*?date|no.*?date',text).group()
    # invoice_number = re.sub(r'(?si)Invoice No. :|date|No. :','',invoice_number).strip()
    invoice_number = re.search(r'(?si)\w+\/\d{4}\-\d{2}\/\d+',invoice_number).group()
    # print('invoice_number :',invoice_number,'\n\n')

    invoice_date = re.search(r'(?si)invoice no.*?seller|no.*?seller',text).group()
    invoice_date = re.search(r'(?si)\d+\.\d+\.\d{3,4}|\d+\-\d+\-\d{3,4}|\d+\.\s\d+\.\s\d{3,4}',text).group()
    # print('invoice_date :',invoice_date,'\n\n')

    check_invoice_status = fetching_invoice_number(db_conn,invoice_number)
    # print('check_invoice_status :',check_invoice_status)
    if check_invoice_status == None:
        # print('error in database')
        return 
    
    if check_invoice_status:
        # print('this invoice already present in database,duplicate invoice')
        return 'already present'
    

    for_buyer_detail = re.search(r'(?si)buyer.*?description',text).group()
    # print('for_buyer_detail :',for_buyer_detail)

   
    try:
        buyer_pan = re.search(r'(?si)pan.*?cst',for_buyer_detail).group()
        buyer_pan = re.search(r'(?si)[A-Z0-9]{5,}',buyer_pan).group()
    except:
        buyer_pan = ''
    # print('buyer_pan :',buyer_pan)

    buyer_tin = re.search(r'(?si)service\stax\sno.*?pan',for_buyer_detail).group()
    buyer_tin = re.search(r'(?si)[0-9]{9,}',for_buyer_detail).group()
    # print('buyer_tin :',buyer_tin)
    
    try:
        buyer_service_tax_no = re.search(r'(?si)service\stax\sno.*?tin',for_buyer_detail).group()
        buyer_service_tax_no = re.search(r'(?si)[A-Z0-9]{10,}',buyer_service_tax_no).group()
        
    except:
        buyer_service_tax_no = ''
    # print('buyer_service_tax_no :',buyer_service_tax_no)

    buyer_cst = re.search(r'(?si)cst.*?description',for_buyer_detail).group()
    buyer_cst = re.search(r'(?si)[0-9]{5,}',buyer_cst).group()
    # print('buyer_cst :',buyer_cst)


    for_seller_detail = re.search(r'(?si)seller.*?Pre(\-|\s)Authenticated',text).group()
    # print('for_seller_detail :',for_seller_detail)


    seller_pan = re.search(r'(?si)pan.*?tin',for_seller_detail).group()
    seller_pan = re.search(r'(?si)[A-Z0-9]{5,}',seller_pan).group()
    # print('seller_pan :',seller_pan)

    seller_tin = re.search(r'(?si)tin.*?service\stax',for_seller_detail).group()
    seller_tin = re.search(r'(?si)[A-Z0-9]{5,}',seller_tin).group()
    # print('seller_tin :',seller_tin)

    seller_service_tax = re.search(r'(?si)service\sTax\sNo.*?cst',for_seller_detail).group()
    seller_service_tax = re.search(r'(?si)[A-Z0-9]{9,}',seller_service_tax).group()
    # print('seller_service_tax :',seller_service_tax)

    seller_cst = re.search(r'(?si)service\sTax\sNo.*?pre(\-|\s)authenticated',for_seller_detail).group()
    seller_cst = re.search(r'(?si)[0-9]{9,}',seller_cst).group()
    # print('seller_cst :',seller_cst)

    

    main_des,line_itmes = pretty_text_data(output_folder)
    # print('main_des :',main_des)
    # print('line_itmes :',line_itmes,'\n\n')

    patch1 = re.search(r'(?si)invoice\samount.*?(note|gross)|subtotal\s+.*?services\:|invoice\samount.*?above\ssale',text).group()
    # print("patch 1",patch1,"\n")

   
    pkg_value = re.sub(r'(?si).*?[0-9,.]{3,}|note.*|ste: The above sale.*|N - e: The above sale|Center Gross|verified|N. The above.*|`e: The above.*',"",patch1)
    # print("pkg value :",pkg_value)


    supply_civil_service = ''
    try:
        # supply_civil_service_pattern = re.search(r'(?si)cst\sno.*?(vehicle|vehicale)',text).group()
        supply_civil_service_pattern = re.search(r'(?si)(cst\sno|pre\-authenticated).*?(vehicle|vehicale)',text).group()
        type1 = ['supply','civil','service']
        for value in type1:
            if value in supply_civil_service_pattern.lower():
                # print('yess present ',value)
                supply_civil_service = value.upper()
    except:
        pass

    # print('supply_civil_service :',supply_civil_service,'\n\n')
    try:
        patch2 = re.search(r'(?si)less\s+\:\s+Retention\s+.*?net\s+|less\sretention.*?(net\svalue|net\sreceivable)',text).group()
        # retention = re.search(r'(?si)([0-9,.]+)\s+',patch2).group()
        retention = re.findall(r'(?si)([0-9,.]+)\s+',patch2)[-1]
        
    except:
        retention = ''
    # print('retention :',retention,'\n\n')
        
    # patch3 = re.search(r'(?si)net\s+Value\s+.*?Amount|net\s+Value\s+.*?words|net\sreceivable\svalue.*?net\samount',text).group()
    patch3 = re.search(r'(?si)net\s+Value\s+.*?Amount|net\s+Value\s+.*?words|(net\sreceivable\svalue|net\sreceviable\svalue).*?net\samount',text).group()
    net_value = re.search(r'(?si)([0-9,.]+)\s+',patch3).group(1)
    # print('net value :',net_value,'\n\n')


    gross_value = re.search(r'(?si)gross\svalue.*?(less\samount|less)',text).group()
    gross_value = re.findall(r'[0-9,.]+',gross_value)
    gross_value = get_num(gross_value)
    # print(gross_value,"?????")
    
    if re.search(r'(?si)less\samount.*?(retention|net)|(less\s\:\samount|less\:\s).*?(retention|net)',text):
        advance_value = re.search(r'(?si)less\samount.*?(retention|net)|(less\s\:\samount|less\:\s).*?(retention|net)',text).group()
        advance_value = re.findall(r'(?si)[0-9,.]+',advance_value)[-1]
    else:
        advance_value = ''
    # print('advance_value :',advance_value)
    

    vat_gst = ''
    vat = ''
    service_tax_gst = ''
    education_cess = ''
    sh_education_cess = ''
    file_name = file_name.split('\\')[-1]

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
            # data= (buyer_name,buyer_address,buyer_pan,buyer_tin,buyer_service_tax_no,buyer_cst,seller_name,seller_address,seller_pan,seller_tin,seller_service_tax,seller_cst,invoice_number,invoice_date,pkg_value.strip(),supply_civil_service,des,unit,qty,rate,amount,'','',gross_value,advance_value,retention,net_value,file_name,timestamp,category)
            data= (buyer_name,buyer_address,buyer_pan,buyer_tin,buyer_service_tax_no,buyer_cst,seller_name,seller_address,seller_pan,seller_tin,seller_service_tax,seller_cst,invoice_number,invoice_date,pkg_value.strip(),supply_civil_service,des,unit,qty,rate,amount,vat_gst,vat,service_tax_gst,education_cess,sh_education_cess,gross_value,advance_value,retention,net_value,file_name,timestamp,category)
            print(1,data,len(data))
            insertGondaExtractions(db_conn,data)
            continue

        
        
        # data= (buyer_name,buyer_address,buyer_pan,buyer_tin,buyer_service_tax_no,buyer_cst,seller_name,seller_address,seller_pan,seller_tin,seller_service_tax,seller_cst,invoice_number,invoice_date,pkg_value.strip(),supply_civil_service,des,unit,qty,rate,amount,'','','','','','',file_name,timestamp,category)
        data= (buyer_name,buyer_address,buyer_pan,buyer_tin,buyer_service_tax_no,buyer_cst,seller_name,seller_address,seller_pan,seller_tin,seller_service_tax,seller_cst,invoice_number,invoice_date,pkg_value.strip(),supply_civil_service,des,unit,qty,rate,amount,'','','','','','','','','',file_name,timestamp,category)
        print(data,len(data))

        insertGondaExtractions(db_conn,data)
    
    return 'success'


    

