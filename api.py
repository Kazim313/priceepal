import requests
import json
import os
import yaml

def load_api_keys():
    with open("static/api_keys.yaml", "r") as file:
        api_keys = yaml.safe_load(file)
    return api_keys

def amazon_api(search_term):
    api_keys = load_api_keys()
    
    # Amazon API  https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-amazon-data/
    url = "https://real-time-amazon-data.p.rapidapi.com/search"

    querystring = {"query": search_term, "page": "1", "country": "US", "category_id": "aps"}
    headers = {
        "X-RapidAPI-Key": api_keys["amazon_api_key"],
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        json_content = response.json()

        path = os.path.dirname(__file__)
        json_file_path = os.path.join(f'{path}\static', 'amazon.json')

        if os.path.exists(json_file_path):
            os.remove(json_file_path)
        
        with open(json_file_path, 'w') as file:
            json.dump(json_content, file)

        print(f"JSON data has been saved to {json_file_path}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def ali_express_api(search_term):
    api_keys = load_api_keys()
    
    # Ali Express API https://rapidapi.com/ecommdatahub/api/aliexpress-datahub/
    url = "https://aliexpress-datahub.p.rapidapi.com/item_search"
    querystring = {"q": search_term, "page": "1"}
    
    headers = {
        "X-RapidAPI-Key": api_keys["ali_express_api_key"],
        "X-RapidAPI-Host": "aliexpress-datahub.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        json_content = response.json()

        path = os.path.dirname(__file__)
        json_file_path = os.path.join(f'{path}\static', 'ali_express.json')
    
        if os.path.exists(json_file_path):
            os.remove(json_file_path)

        with open(json_file_path, 'w') as file:
            json.dump(json_content, file)

        print(f"JSON data has been saved to {json_file_path}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def download_data(search):
    amazon_api(search)
    ali_express_api(search)
