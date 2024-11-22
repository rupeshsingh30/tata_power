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
            if 'Description' in line or 'Quantity' in line or 'Qty' in line or 'Invoice Amount' in line:
                headers_skipped = True
            continue

        table1 = line.split('|')[1:-1]
        # print(table1,">>>>")

        try:
            zero_postion = re.sub(r'(?si)category\sof\sservice.*|egory|\( gory.*',"",table1[0])
            table1[0] = zero_postion.strip()
        except:
            pass

        if len(table1) == 5:
            if table1[0].strip()!= '' and table1[1].strip()== '' and table1[2].strip() == '' and table1[3].strip() == '' and table1[4].strip() == '':
                main_des.append(table1[0])
                continue

            elif (table1[1].strip() == '' and table1[-1].strip() == '') or (table1[0].strip() == ''):
                continue
            elif table1[1].strip() == '' and table1[3].strip() == '' and table1[-1].strip() != '':
                continue
            elif table1[1].strip() != '' and (table1[3].strip() == '' or table1[3].strip() != '') and table1[-1].strip() == '':
                continue
            elif table1[0].strip() != '' and (table1[3].strip() != ''):
                continue
            # elif re.search(r'pkg|pkg\-[0-9]+|pkg\s+\-[0-9]+', table1[0].strip(), re.IGNORECASE):
            #     continue
            elif 'Add' in table1[1] or ' S.Tax' in table1[1] or 'S. Tax' in table1[1]:
                continue

            # print(table1,">>>>")
            line_item = {
                'description': table1[0].strip(),
                'quantity': table1[1].strip(),
                'unit': '',
                'rate': table1[2].strip(),
                'amount': table1[4].strip()
            }

            line_items.append(line_item)

    return main_des,line_items
def type2(data):
    main_des = []
    line_items = []
    headers_skipped = False
    for line in data:
        if not headers_skipped:
            if 'Description' in line or 'Quantity' in line or 'Qty' in line or 'Invoice Amount' in line:
                headers_skipped = True
            continue

        table1 = line.split('|')[1:-1]
        # print(table1,">>>>",len(table1))

        try:
            zero_postion = re.sub(r'(?si)category\sof\sservice.*|egory|\( gory.*',"",table1[0])
            table1[0] = zero_postion.strip()
        except:
            pass
        
        if len(table1) == 6:
            
            if table1[0].strip()!= '' and table1[1].strip()== '' and table1[2].strip() == '' and table1[3].strip() == '' and table1[4].strip() == '' and table1[5].strip() == '':
                main_des.append(table1[0])
                continue

            elif 'Verified' in table1[0] or (table1[0].strip()=='' and table1[1].strip()==''):
                continue
            elif table1[0].strip() != "" and table1[1].strip() == '' and table1[2].strip() == '':
                continue
            elif table1[0].strip()=='' and 'Less' in table1[1]:
                continue
            # elif re.search(r'pkg|pkg\-[0-9]+|pkg\s+\-[0-9]+', table1[0].strip(), re.IGNORECASE):
            #     continue
             
            

            if table1[0].strip() != '' and table1[4].strip() == '':
                line_item = {
                    'description': table1[0].strip(),
                    'unit': table1[1].strip(),
                    'quantity': table1[2].strip(),
                    'rate': table1[3].strip(),
                    'amount': table1[5].strip()
                }

                line_items.append(line_item)

        if len(table1) == 5:
            
            if table1[0].strip()!= '' and table1[1].strip()== '' and table1[2].strip() == '' and table1[3].strip() == '' and table1[4].strip() == '':
                main_des.append(table1[0])
                continue

            elif 'Verified' in table1[0] or (table1[0].strip()=='' and table1[1].strip()==''):
                continue
            elif table1[0].strip() != "" and table1[1].strip() == '' and table1[2].strip() == '':
                continue
            elif table1[0].strip()=='' and 'Less' in table1[1]:
                continue
            

            if table1[0].strip() != '':
                line_item = {
                    'description': table1[0].strip(),
                    'unit': table1[1].strip(),
                    'quantity': table1[2].strip(),
                    'rate': table1[3].strip(),
                    'amount': table1[4].strip()
                }

                line_items.append(line_item)

    return main_des,line_items


def type3(data):
    main_des = []
    line_items = []
    headers_skipped = False
    for line in data:
        if not headers_skipped:
            if 'DETAILS' in line or 'AMOUNT' in line or 'S.NO' in line:
                headers_skipped = True
            continue

        table1 = line.split('|')[1:-1]
        # print(table1,">>>>",len(table1))

        if len(table1) == 4:

            if 'total' in table1[1].lower():
                break
            
            if table1[0].strip() != '':
                line_item = {
                    'description': table1[1].strip(),
                    'unit': '',
                    'quantity': '',
                    'rate': '',
                    'amount': table1[-1].strip()
                }

                line_items.append(line_item)

    return main_des,line_items


def aws_pretty_text(output_folder,text):

    for file in os.listdir(output_folder):
        if file.endswith('pretty.txt'):
            with open(os.path.join(output_folder, file), 'r', encoding="utf-8") as raw_data:
                data = raw_data.readlines()
            data2 = ' '.join(data)
            # print(data2,"??")
            if ('Description of Supply / Services' in data2 and 'Quantity' in data2 and 'Unit Rate (INR)' in data2 and 'Total Amount' in data2):
                print('condition 1')
                a = type1(data)
                return a
            elif ('Description of Supply / Services' in data2 and 'Unit' in data2 and 'Quantity' in data2 and 'Unit Rate (INR)' in data2 and 'Amount' in data2) or ('Description of Supply / Services' in data2 and 'Unit' in data2 and 'Quantity' in data2 and 'Unit Rate' in data2 and 'Amount (INR)' in data2):
                print('condition 2')
                a = type2(data)
                return a
            elif ('DETAILS' in data2 and 'AMOUNT' in data2):
                print('conditon 3')
                a = type3(data)
                return a
            



def tax_invoice(file_name,text,res_para,output_folder,db_conn,category,excel_id):
    # print(text,'\n\n')
    
    time_stamp = datetime.now()

    invoice_number = re.search(r'(?si)invoice\sno.*?date',text).group()
    try:
        invoice_number = re.search(r'(?si)[A-Za-z]+\/.*?\/[0-9]+\s',invoice_number).group().strip()
    except:
        invoice_number = re.sub(r'(?si)Invoice No(\.\s\:|\.)|Date|Vibhuti Khand\,|Gomati Nagar\,|invoice',"",invoice_number).strip()
    # print('invoice_number :',invoice_number,'\n\n')

    invoice_date = re.search(r'(?si)date.*?seller|invoice\sdate.*?description',text).group()
    if re.search(r'(?si)\d+(\.|\/|\-)\d+(\.|\/|\-)\d{3,4}',invoice_date):
        invoice_date = re.search(r'(?si)\d+(\.|\/|\-)\d+(\.|\/|\-)\d{3,4}',invoice_date).group()
    elif re.search(r'(?si)\d+\.\d+\.\d{2,4}',invoice_date):
        invoice_date = re.search(r'(?si)\d+\.\d+\.\d{2,4}',invoice_date).group()
    # print('invoice_date :',invoice_date,'\n\n')

    check_invoice_status = fetching_invoice_number(db_conn,invoice_number)
    # print('check_invoice_status :',check_invoice_status,'\n\n')
    if check_invoice_status == None:
        # print('error in database')
        return 
    
    if check_invoice_status:
        # print('this invoice already present in database,duplicate invoice')
        return 'already present'


    schema, prompt = api_schema()
    result = ask_qa(text,prompt,schema)   ### QNA API.....
    
    # try:
    #     result = json.loads(result)
    # except:
    #     result = ''
    # print('result :',result,"\n\n")
        
    # if result == '504.0 GatewayTimeout':
    #     result = ask_qa(text,prompt,schema)

    # if result["buyerName"] == '' or  result["buyerAddress"] == '' or result['vendorName'] == '' or result['vendorAddress'] == '':
    #     result = ask_qa(text,prompt,schema)
    
    # if result["buyerName"] == None or  result["buyerAddress"] == None or result['vendorName'] == None or result['vendorAddress'] == None:
    #     result = ask_qa(text,prompt,schema)

    # print('result :-',result)
    if result == {}:
        result = ask_qa(text,prompt,schema)

    print('result :-',result)
    
    try:
        # buyer_name = result["buyerName"]
        buyer_name = 'South East UP Power Transmission Co. Ltd.'
    except:
        buyer_name = ''
    
    try:
        buyer_address = result["buyerAddress"]
        # buyer_address = '601,602, Shalimar Titanium, 6th Floor, Plot No. TC G 1/1, Near Gandhi Pratiishthan, Vibhuti Khand, Gomti Nagar, Lucknow.'
    except:
        buyer_address = ''

    try:
        seller_name = result['vendorName']
    except:
        seller_name = ''

    try:
        
        seller_address = result['vendorAddress']
        # seller_address = '601,602, Shalimar Titanium, 6th Floor, Plot No. TC G 1/1, Near Indira Gandhi Pratiishthan, Vibhuti Khand, Gomti Nagar, Lucknow.'
    except:
        seller_address = ''
    # print(buyer_name,buyer_address,">>",seller_name,seller_address,"\n")
    
    

    ### buyer details 
    try:
        for_buyer_detail = re.search(r'(?si)buyer.*?description',text).group()
    except:
        for_buyer_detail = ''
    # print('for_buyer_detail :',for_buyer_detail,'\n\n')

    try:
        buyer_pan = re.search(r'(?si)pan.*?cst',for_buyer_detail).group()
        buyer_pan = re.search(r'(?si)[A-Z0-9]{5,}',buyer_pan).group()
    except:
        buyer_pan = ''
    # print('buyer_pan :',buyer_pan,'\n\n')

    try:
        buyer_tin = re.search(r'(?si)service\stax.*?pan',for_buyer_detail).group()
        buyer_tin = re.search(r'(?si)[0-9]{9,}',for_buyer_detail).group()
    except:
        buyer_tin = ''
    # print('buyer_tin :',buyer_tin,'\n\n')

    try:
        buyer_service_tax_no = re.search(r'(?si)service\stax\sno.*?tin',for_buyer_detail).group()
        buyer_service_tax_no = re.search(r'(?si)[A-Z0-9]{10,}',buyer_service_tax_no).group()
        
    except:
        buyer_service_tax_no = ''
    # print('buyer_service_tax_no :',buyer_service_tax_no,'\n\n')

    try:
        buyer_cst = re.search(r'(?si)cst.*?description',for_buyer_detail).group()
        buyer_cst = re.search(r'(?si)[0-9]{5,}',buyer_cst).group()
    except:
        buyer_cst = ''
    # print('buyer_cst :',buyer_cst,'\n\n')

    ###seller details
    try:
        for_seller_detail = re.search(r'(?si)seller.*?(Pre-Authenticated|buyer)',text).group()
    except:
        for_seller_detail = ''
    # print('for_seller_detail :',for_seller_detail)

    try:
        seller_pan = re.search(r'(?si)pan.*?tin',for_seller_detail).group()
        seller_pan = re.search(r'(?si)[A-Z0-9]{5,}',seller_pan).group()
    except:
        seller_pan = ''
    # print('seller_pan :',seller_pan,'\n\n')

    try:
        seller_tin = re.search(r'(?si)tin.*?service\stax',for_seller_detail).group()
        seller_tin = re.search(r'(?si)[A-Z0-9]{5,}',seller_tin).group()
    except:
        seller_tin = ''
    # print('seller_tin :',seller_tin,'\n\n')

    try:
        seller_service_tax = re.search(r'(?si)service\sTax\sNo.*?(cst|pre-authenticated)',for_seller_detail).group()
        seller_service_tax = re.search(r'(?si)[A-Z0-9]{9,}',seller_service_tax).group()
    except:
        seller_service_tax = ''
    # print('seller_service_tax :',seller_service_tax,'\n\n')

    try:
        seller_cst = re.search(r'(?si)cst.*?(pre-authenticated|buyer)',for_seller_detail).group()
        seller_cst = re.search(r'(?si)[0-9]{9,}',seller_cst).group()
    except:
        seller_cst = ''
    # print('seller_cst :',seller_cst,'\n\n')

    ######### To find Substation Name / Net Value / Less Retention........
    
    supply_civil_service = ''

    try:
        supply_civil_service_pattern = re.search(r'(?si)(cst\sno|pre\-authenticated).*?(authorise|vehicle)',text).group()
    except:
        supply_civil_service_pattern = ''

    # print(supply_civil_service_pattern,"????")
    type1 = ['supply','civil','service']
    for value in type1:
        if value in supply_civil_service_pattern.lower():
            supply_civil_service = value.upper()
            break
    print('supply_civil_service :',supply_civil_service,'\n\n')
    
    vat = ''
    education_cess = ''
    he_education_cess = ''
    vat_gst = ''
    service_tax = ''
    gross_value = ''
    retention = ''
    net_value = ''

    if supply_civil_service_pattern == "":
        pkg_value = ''
        gross_value = ''
        advance_value = ''
        retention = ''
        net_value = ''
        service_tax = ''
        vat_gst = ''

        try:
            vat_gst = re.search(r'(?si)add\svat\s\@.*?gross\svalue',text).group()
            vat_gst = re.findall(r'(?si)[0-9,.]+',vat_gst)[-1]
        except:
            vat_gst = ''
        print('vat_gst :',vat_gst,'\n\n')

        try:
            gross_value = re.search(r'(?si)total.*?service\stax',text).group()
            gross_value = re.findall(r'(?si)[0-9,.]+',gross_value)[-1]
        except:
            gross_value = ''
        # print('gross_value :',gross_value,'\n\n')

        try:
            service_tax = re.search(r'(?si)service\stax.*?education\scess',text).group()
            service_tax = re.findall(r'(?si)[0-9,.]+',service_tax)[-1]
        except:
            service_tax = ''
        # print('service_tax :',service_tax,'\n\n')

        try:
            education_cess = re.search(r'(?si)education\scess.*?s\.h\.e\.c',text).group()
            education_cess = re.sub(r'(?si)s\.h\.e\.c',"",education_cess)
            education_cess = re.findall(r'[0-9,.]+',education_cess)[-1]
        except:
            education_cess = ''
        # print('education cess :',education_cess,'\n\n')

        try:
            he_education_cess = re.search(r'(?si)s\.h\.e\.c.*?total',text).group()
            he_education_cess = re.findall(r'[0-9,.]+',he_education_cess)[-1]
        except:
            he_education_cess = ''
        # print('he_education_cess :',he_education_cess,'\n\n')
    
        try:
            net_value = re.search(r'(?si)total.*?approved\sby',text).group()
            net_value = re.findall(r'(?si)[0-9,.]+',net_value)[-1]
        except:
            net_value = ''
        # print('net_value :',net_value,'\n\n')

        # print('no suplly civil service present')


    elif supply_civil_service.lower() == 'civil' :
        patch1 = re.search(r'(?si)subtotal\s+.*?category\s+|subtotal\s+.*?services\:',text).group()
        # print(patch1,">>>>")
        pattern = r"Tax @.*?Category|Tax a.*?Category"
        match = re.search(pattern, patch1)
        
        if match:
            result = match.group(0)
            result = re.sub(r'(?si)Tax\s+(\@\s|\@|a\s)+.*?[0-9,]+\s+[0-9,.]+\s+','',result).strip()
            pkg_value = result.replace("Category", "").strip()
            # print('pkg_value : ',pkg_value,'\n\n')

        gross_value = re.search(r'(?si)gross\svalue.*?(less\samount|less|amount)',text).group()
        gross_value = re.findall(r'[0-9,.]+',gross_value)[-1]
        # print('gross_value :',gross_value,'\n\n')


        if re.search(r'(?si)(less\s\:\smobilization\sadvance|less\s\:\smobilisation\sadvance|less\smobilization\sadvance|less\smobilisation\sadvance).*?(net\svalue|net\sreceivable\svalue)',text):
            advance_value = re.search(r'(?si)(less\s\:\smobilization\sadvance|less\s\:\smobilisation\sadvance|less\smobilization\sadvance|less\smobilisation\sadvance).*?(net\svalue|net\sreceivable\svalue)',text).group()
            advance_value = re.findall(r'(?si)[0-9,.]+',advance_value)[-1]
        else:
            advance_value = ''
        # print('advance_value :',advance_value,'\n\n')


        if re.search(r'(?si)less(\s+\:\s+|\s)Retention\s+.*?(less\s\:\smobilization\sadvance|less\s\:\smobilisation\sadvance|less\smobilization\sadvance|less\smobilisation\sadvance)',text):
            retention = re.search(r'(?si)less(\s+\:\s+|\s)Retention\s+.*?(less\s\:\smobilization\sadvance|less\s\:\smobilisation\sadvance|less\smobilization\sadvance|less\smobilisation\sadvance)',text).group()
            retention = re.findall(r'(?si)([0-9,.]+)\s+',retention)[-1]
            # print('retention :',retention,'\n\n')
        elif re.search(r'(?si)less\s+\:\s+Retention\s+.*?net\s+|less\:\s+Retention\s+.*?net\s+',text):
            retention = re.search(r'(?si)less\s+\:\s+Retention\s+.*?net\s+|less\:\s+Retention\s+.*?net\s+',text).group()
            retention = re.findall(r'(?si)([0-9,.]+)\s+',retention)[-1]
        else:
            retention = ''
        # print('retention :',retention,'\n\n')

        if re.search(r'(?si)net\s+Value\s+.*?Amount|(net\s+Value\s+|net\sreceivable\svalue).*?words',text):
            net_value = re.search(r'(?si)net\s+Value\s+.*?Amount|(net\s+Value\s+|net\sreceivable\svalue).*?words',text).group()
            net_value = re.findall(r'(?si)([0-9,.]+)\s+',net_value)[-1]
        else:
            net_value = ''
        # print('net_value :',net_value,'\n\n')

        try:
            patch4 = re.search(r'(?si)subtotal\s+.*?category\s+|subtotal\s+.*?services\:',text).group()
            patch4 = re.search(r'(?si)Sub\s+Total\s+[0-9,.]+.*?Add',patch4).group()
            vat_gst = re.findall(r'(?si)[0-9,]+',patch4)[-1]
        except:
            vat_gst = ''
        # print('Vat Gst : ',vat_gst,'\n\n')

        
        patch5 = re.search(r'(?si)subtotal\s+.*?category\s+|subtotal\s+.*?services\:',text).group()
        patch5 = re.search(r'(?si)Tax\s+\@\s+.*?Category|Tax\s+\@.*?Category|Tax\s+a.*?Category',patch5).group()
        service_tax = re.findall(r'(?si)[0-9,]{3,}',patch5)[-1].strip()
        # print('Service Tax : ',service_tax,'\n\n')

    
    elif supply_civil_service.lower() == 'service' :
        print('service ---------------------------------')

        try:
            pkg_value = re.search(r'(?si)invoice\samount.*?(category\sof\sservice|of\sservice)',text).group()
            pkg_value = re.sub(r'(?si).*?[0-9,.]{3,}|category.*|Annexure|vegory of Service|egory of Service|\+egory of Service|\( gory of Service|Ca\' of Service',"",pkg_value).strip()
        except:
            pkg_value = ''
        print("pkg value :",pkg_value,'\n\n')

        vat_gst = ''
        print('vat_gst :',vat_gst,'\n\n')

        if re.search(r'(?si)add\:\sservice\stax.*?gross\svalue',text):
            service_tax = re.search(r'(?si)add\:\sservice\stax.*?gross\svalue',text).group()
            service_tax = re.findall(r'[0-9,.]+',service_tax)[-1]
        elif re.search(r'(?si)add\:\sservice\stax.*?g\.\stotal',text):
            service_tax = re.search(r'(?si)add\:\sservice\stax.*?g\.\stotal',text).group()
            service_tax = re.sub(r'(?si)g\.\stotal',"",service_tax)
            service_tax = re.findall(r'[0-9,.]+',service_tax)[-1]
        else:
            service_tax = ''
        # print('servive tax :',service_tax,'\n\n')

        if re.search(r'(?si)gross\svalue.*?less',text):
            gross_value = re.search(r'(?si)gross\svalue.*?less',text).group()
            gross_value = re.findall(r'[0-9,.]+',gross_value)[-1]
        elif re.search(r'(?si)g\.\stotal.*?amount',text):
            gross_value = re.search(r'(?si)g\.\stotal.*?amount',text).group()
            gross_value = re.findall(r'[0-9,.]+',gross_value)[-1]
        else:
            gross_value = ''
        # print('gross_value :',gross_value,'\n\n')

        if re.search(r'(?si)(less\s\:\sretention|less\:retention|less retention).*?(less\s:\smobilisation|less\smobilisation)',text):
            retention = re.search(r'(?si)(less\s\:\sretention|less\:retention|less retention).*?(less\s:\smobilisation|less\smobilisation)',text).group()
            retention = re.findall(r'[0-9,.]+',retention)[-1]
        else:
            retention = ''
        # print('retention :',retention,'\n\n')

        if re.search(r'(?si)(less\s\:\smobilisation\sadvance|less\smobilisation\sadvance).*?net',text):
            advance_value = re.search(r'(?si)(less\s\:\smobilisation\sadvance|less\smobilisation\sadvance).*?net',text).group()
            advance_value = re.findall(r'[0-9,.]+',advance_value)[-1]
        else:
            advance_value = ''
        # print('advance_value :',advance_value,'\n\n')

        if re.search(r'(?si)(net\svalue|net\sreceivable\svalue).*?(net\samount|amount)',text):
            net_value = re.search(r'(?si)(net\svalue|net\sreceivable\svalue).*?(net\samount|amount)',text).group()
            net_value = re.findall(r'[0-9,.]+',net_value)[-1]
        else:
            net_value = ''
        # print('net_value :',net_value,'\n\n')
        
    elif supply_civil_service.lower() == 'supply' :
        print('supply -------------')
        
        pkg_value = re.search(r'(?si)invoice\samount.*?gross\svalue',text).group()
        pkg_value = re.sub(r'(?si).*?[0-9,.]{3,}|gross.*|note.*|Add VAT [0-9]+\%',"",pkg_value).strip()
        # print("pkg value :",pkg_value,'\n\n')

        try:
            if re.search(r'(?si)vat\s(\@|a).*?(additional\svat|add\:\sadd\.\svat)',text):
                vat_gst = re.search(r'(?si)vat\s(\@|a).*?(additional\svat|add\:\sadd\.\svat)',text).group()
                vat_gst = re.sub(r'(?si)add: add. vat',"",vat_gst)
                vat_gst = re.findall(r'(?si)[0-9,.]+',vat_gst)[-1]
            elif re.search(r'(?si)add(\:\s|\s)vat\s(\@|\(a).*?gross\svalue',text):
                vat_gst = re.search(r'(?si)add(\:\s|\s)vat\s(\@|\(a).*?gross\svalue',text).group()
                vat_gst = re.sub(r'(?si)add: add. vat',"",vat_gst)
                vat_gst = re.findall(r'(?si)[0-9,.]+',vat_gst)[1]
            
        except:
            vat_gst = ''
        print('vat_gst :',vat_gst,'\n\n')
            
        try:
            vat = re.search(r'(?si)(additional\svat|add\:\sadd\.\svat).*?gross\svalue',text).group()
            vat = re.sub(r'(?si)add: add. vat',"",vat)
            vat = re.findall(r'(?si)[0-9,.]+',vat)[1]
        except:
            vat = ''
        # print('vat :',vat,'\n\n')

        service_tax = ''
        # print('service tax :',service_tax,'\n\n')

        gross_value = re.search(r'(?si)gross\svalue.*?less',text).group()
        gross_value = re.findall(r'[0-9,.]+',gross_value)[-1]
        # print('gross_value :',gross_value,'\n\n')

        advance_value = re.search(r'(?si)(less\samount|less\s\:\samount|less\:\samount).*?less\s\:\sretention',text).group()
        advance_value = re.findall(r'[0-9,.]+',advance_value)[-1]
        # print('advance_value :',advance_value,'\n\n')

        retention = re.search(r'(?si)less\s\:\sretention.*?(net\svalue|net\sreceivable)',text).group()
        retention = re.findall(r'[0-9,.]+',retention)[-1]
        # print('retention :',retention,'\n\n')
        
        net_value = re.search(r'(?si)(net\svalue|net\sreceivable).*?(net\samount|amount)',text).group()
        net_value = re.findall(r'[0-9,.]+',net_value)[-1]
        # print('net_value :',net_value,'\n\n')


   

    ### for line item 
    main_des,line_items = aws_pretty_text(output_folder,text)

    print('main_des :',main_des,'\n\n')
    print('line_items :',line_items,'\n\n')

    if main_des == [] and line_items == []:
        return 'error'


    file_name = file_name.split('\\')[-1]
    
    for index,line_item in enumerate(line_items):

        if main_des == []:
            des = line_item['description']

        elif main_des != []:
            des = str(main_des[0].strip()) + " " + str(line_item['description'])


        des = des.replace(pkg_value.strip(),"").replace('"Erection, Commissioning & Installation"',"").strip()
        des = re.sub(r'(?si)add\svat.*',"",des).strip()
        qty = line_item['quantity'].strip()
        unit = line_item['unit'].strip()
        rate = line_item['rate'].strip()
        amount = line_item['amount'].strip()


        if index == 0 :
            data= (buyer_name,buyer_address,buyer_pan,buyer_tin,buyer_service_tax_no,buyer_cst,seller_name,seller_address,seller_pan,seller_tin,seller_service_tax,seller_cst,invoice_number,invoice_date,pkg_value,supply_civil_service,des,unit,qty,rate,amount,vat_gst,vat,service_tax,education_cess,he_education_cess,gross_value,advance_value,retention,net_value,file_name,time_stamp,category)
            print(data,len(data))
            insertGondaExtractions(db_conn,data)
            continue


       
        data= (buyer_name,buyer_address,buyer_pan,buyer_tin,buyer_service_tax_no,buyer_cst,seller_name,seller_address,seller_pan,seller_tin,seller_service_tax,seller_cst,invoice_number,invoice_date,pkg_value,supply_civil_service,des,unit,qty,rate,amount,'','','',education_cess,he_education_cess,'','','','',file_name,time_stamp,category)
        print(data,len(data))
        insertGondaExtractions(db_conn,data)

        # print("-----------------------------------------------------------")

    return 'success'