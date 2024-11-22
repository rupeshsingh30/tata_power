import os
import json
import requests

# def call_qa_api(filepath,text,prompt_to_check,schema):
def call_qa_api(text,prompt_to_check,schema):

    url = "https://sequeldocapi.azurewebsites.net/api/sequelAI?code=94wT9VZ9KgTJbFJDC1SKBHqdET4CGVLromQS02ZH6zToAzFuGksFqA=="

    try:
        # Make the POST request with file contents as data
        json_data1 = {
                "type": "qa",
                "text": text,
                "prompt": prompt_to_check,
                "parse": False
            }

        json_data2 = json.dumps(json_data1)

        response = requests.post(url, data=json_data2, headers={"Content-type":"application/json"})
       
        return response.text


    except requests.exceptions.RequestException as e:
        print("An error occurred while making the POST request:", e)
        return None
    except json.JSONDecodeError as e:
        print("An error occurred while parsing the JSON response:", e)
        return None
    except IOError as e:
        print("An error occurred while writing the JSON response to a file:", e)
        return None


def ask_qa(data,prompt,schema):
    
    # response = call_qa_api(file_path,data,prompt,schema)
    response = call_qa_api(data,prompt,schema)
    # print('respone :',response)
    try:
        response = json.loads(response)
    except:
        response = {}


    return response





def api_schema():
 
    schema = {
        # Your schema structure goes here
    }

    prompt = '''{
        "buyerName": "Extract the buyer's name from the invoice text.",
        "buyerAddress": "Extract the buyer's address from the invoice text.",
        "vendorName": "Extract the vendor's name from the invoice text.",
        "vendorAddress": "Extract the vendor's address (usually the first address listed but not pick to or buyer) from the invoice text.",
        "invoice_number": "Extract the invoice number from the invoice text.",
        "invoice_date": "Extract the invoice date from the invoice text."
    }'''
    # prompt = '''{
    #     "buyerName": "Extract the buyer's name from the invoice text. if buyer's name is not present return 'not mentioned' ",
    #     "buyerAddress": "Extract the buyer's address from the invoice text. if buyer's address is not present return 'not mentioned",
    #     "vendorName": "Extract the vendor's name from the invoice text. if vendor's name is not present return 'not mentioned",
    #     "vendorAddress": "Extract the vendor's address (usually the first address listed but not pick to or buyer) from the invoice text.if vendor's address is not present return 'not mentioned",
    #     "invoice_number": "Extract the invoice number from the invoice text.",
    #     "invoice_date": "Extract the invoice date from the invoice text."
    # }'''

    # prompt = '''{
    # "buyerName": "Extract the buyer's name from the buyer details section in the invoice text.",
    # "buyerAddress": "Extract the buyer's address from the buyer details section only, from fields specified for buyer, in the invoice text.",
    # "vendorName": "Extract the vendor's name from the vendor details section in the invoice text.",
    # "vendorAddress": "Extract the vendor's address (usually the first address listed but not pick to or buyer) from the vendor details section only, avoiding any addresses associated with the buyer, in the invoice text.",
    # "invoice_number": "Extract the invoice number from the invoice text.",
    # "invoice_date": "Extract the invoice date from the invoice text."
    # }'''


    return schema, prompt
