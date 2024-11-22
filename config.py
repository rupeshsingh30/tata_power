
import json
def loadConfig(config_file_name):
    try:
        # Open and read the config file
        with open(config_file_name, 'r') as config_file:
            # Parse the JSON data
            return json.load(config_file)
    except Exception as e:
        print("Error loading config file:", e)

    


