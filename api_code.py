import json
import requests


schema = {
    "fields": { 
   
    },
    "table": {
        
    }
}


def trigger_sequeldocapi(filePath,schema=schema):
 
    def file_to_uint8array_string(fileName):
        with open(fileName, "rb") as file:
            data = file.read()
        uint8_array = [str(byte) for byte in data]
        uint8_array_string = "[" + ", ".join(uint8_array) + "]"
        return uint8_array_string
    
    final_array = file_to_uint8array_string(filePath)
   
    sample = {"file": final_array, "settings": {
                "filter": True,
                "keyvaluePair": True,
                "language": "english",
                "translate": False,
                "multilingual": False,
                "table": {
                        "include": True,
                        "validate": False,
                        "json": True
                },
                "pages": "1-150",
                "paragraphs": {
                        "json": True
                }
            }, "schema":schema,"version": "2.0.0"}
    
    json_data = json.dumps(sample)

    url = "https://sequeldocapi.azurewebsites.net/api/sequelDoc?code=_kma-N8nyRg4TWA9ft_NpHWaHhSMLC6lpW5mmEWezh4IAzFuHZf_1Q=="


    try:
        # Make the POST request with file contents as data
        response = requests.post(url, data=json_data, headers={"Content-type":"application/json"})
        print(response)
        # Parse the JSON string to a Python dictionary
        data = response.json()

        # Convert the response data to a formatted JSON string
        json_str = json.dumps(data, indent=4)

        return data

    except requests.exceptions.RequestException as e:
        print("An error occurred while making the POST request:", e)
        return None
    except json.JSONDecodeError as e:
        print("An error occurred while parsing the JSON response:", e)
        return None  
    except IOError as e:
        print("An error occurred while writing the JSON response to a file:", e)
        return None
    
# filePath = r"C:\Users\Admin\Downloads\A0350002-7.pdf"
# # filePath = r"C:\Users\Admin\Downloads\A0350002-6.pdf"
# res = trigger_sequeldocapi(filePath)
# print(res)
    

