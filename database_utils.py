
import psycopg2
from config import *  
from datetime import datetime
import pandas as pd


# def db_connection():
def dbConnection(config):
    conn = psycopg2.connect(
        dbname=config['db_creds']['database'], 
        user=config['db_creds']['user'],
        password=config['db_creds']['password'],
        host=config['db_creds']['host'],
        port=config['db_creds']['port']
        )
    cursor=conn.cursor()
    conn.rollback()

    return (conn,cursor)


def getExcelId(db_conn):
    conn,cursor = db_conn[0],db_conn[1]
    query = ''' SELECT excel_id FROM file_details
                WHERE excel_id IS NOT NULL
                ORDER BY excel_id DESC
                LIMIT 1
            '''
    cursor.execute(query)

    try:
        excel_id = cursor.fetchone()
        excel_id = excel_id[0]
        # excel_id += 1
    except:
        excel_id = 1

    return excel_id

# config = loadConfig(r'D:\tata_power_gonda\gonda_process\code\app.config')
# db_conn = dbConnection(config)
# excel_id = getExcelId(db_conn)
# print(excel_id)


def fetching_invoice_number(db_conn,invoice_number):
    conn,cursor = db_conn[0],db_conn[1]
    try:
        # query1 = f''' select exists (select * from gonda_extraction_data where invoice_number = '{invoice_number}' ) '''
        query1 = f''' select exists (select * from gonda_extraction11 where invoice_number = '{invoice_number}' ) '''
        cursor.execute(query1)
        status = cursor.fetchone()[0]
    except:
        return None
    
    return status


# invoice_number = 'UPBOOT/2014-15/0004'
# conn,cursor = create_db_connection()
# a = fetching_invoice_number(conn,cursor,invoice_number)
# print(a)


def transform_tuple(data):
    def transform_element(item):
        if isinstance(item, list):
            # Convert list to string with double quotes
            return str(item).replace("'", '"')
        elif item is None:
            # Convert None to the string 'None'
            return 'None'
        elif item == '':
            # Convert empty string to the string 'None'
            # return 'None'
            return ''
        return item
    
    return tuple(transform_element(item) for item in data)



def insertDataFileDetails(dbConn, data):
    conn, cursor = dbConn[0], dbConn[1]
    #print(">>>",data,"<<<",len(data))

    data = transform_tuple(data)
    
    try:
        query = f'''INSERT INTO file_details (execution_id,excel_name,pdf_name_in_excel,page_number_in_excel,actual_pdf_name,split_pdf,status,timestamp,remark)VALUES (
        '{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}', '{data[7]}','{data[8]}'
        )'''
        # cursor.execute(query)
        # conn.commit()
        # print('Inserted in file details')
        
    except:
        conn.rollback()
        query = f'''INSERT INTO file_details (execution_id,excel_name,pdf_name_in_excel,page_number_in_excel,actual_pdf_name,split_pdf,status,timestamp,remark)VALUES (
        '{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}', '{data[7]}','{data[8]}'
        )'''
        # cursor.execute(query)
        # conn.commit()
        # print('Inserted in file details')



def insertGondaExtractions(db_conn,data):

    conn,cursor = db_conn[0],db_conn[1]
    
    try:
        insert_query = '''
        INSERT INTO gonda_extraction11 (
            buyer_name, buyer_address, buyer_pan, buyer_tin, buyer_tax_number, buyer_cst_number, seller_name, seller_address, seller_pan,seller_tin, seller_tax_number, seller_cst_number, invoice_number, invoice_date, pkg_transmission_line_ss_substation_name, supply_civil_services,
            description, unit, quantity, rate, invoice_value, vat_gst,vat, service_tax_gst,education_cess,he_education_cess,gross_value,
            advance, retention, net_value, file_name,timestamp,invoice_type
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''

        cursor.execute(insert_query, data)
        conn.commit()
        print('inserted in database')
    except:
        conn.rollback()
        insert_query = '''
        INSERT INTO gonda_extraction11 (
            buyer_name, buyer_address, buyer_pan, buyer_tin, buyer_tax_number, buyer_cst_number, seller_name, seller_address, seller_pan,seller_tin, seller_tax_number, seller_cst_number, invoice_number, invoice_date, pkg_transmission_line_ss_substation_name, supply_civil_services,
            description, unit, quantity, rate, invoice_value, vat_gst,vat, service_tax_gst,education_cess,he_education_cess,gross_value,
            advance, retention, net_value, file_name,timestamp,invoice_type
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''

        cursor.execute(insert_query, data)
        conn.commit()
        print('inserted in database')


def insertGondaExtractionError(db_conn, excel_id, file_name, status):
    timestamp = datetime.now()
    data = (
         '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '','', '', '',
        file_name, timestamp, status
    )
    insertGondaExtractions(db_conn, data)



def pullReport(report_folder,db_conn):
    
    conn,cursor = db_conn[0],db_conn[1]
    todays_date = str(datetime.now().strftime('%Y-%m-%d'))
    # input_df = pd.read_sql_query(f''' select * from gonda_extraction11 where timestamp like '%{todays_date}%' ''',con=conn)
    input_df = pd.read_sql_query(f''' select * from gonda_extraction11 where invoice_type != 'new format' and invoice_type != 'error' ''',con=conn)
    input_df.to_excel(rf'{report_folder}'+'\\'+'report.xlsx',index=False)



# conn,cursor = create_db_connection()
# report_folder = r'C:\Users\Admin\Downloads\api_code\report'
# pull_data(report_folder,conn)
    

