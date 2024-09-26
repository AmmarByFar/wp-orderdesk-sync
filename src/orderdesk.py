import os
import requests
import csv
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'api_key': os.getenv('ORDERDESK_API_KEY'),
        'store_id': os.getenv('ORDERDESK_STORE_ID')
    }

def get_inventory_items():
    config = load_config()
    API_KEY = config['api_key']
    STORE_ID = config['store_id']
    
    url = "https://app.orderdesk.me/api/v2/inventory-items"
    headers = {
        "ORDERDESK-STORE-ID": STORE_ID,
        "ORDERDESK-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['inventory_items']
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []

def get_orderdesk_print_sku(color: str, size: str):
    with open("D:/Projects/PropCoWebsite/Products/wp-orderdesk-sync/bc3001-skus.csv", 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Color'].lower() == color.lower() and row['Size'].upper() == size.upper():
                return row['SKU']
    return None

def create_inventory_item(product):
    config = load_config()
    API_KEY = config['api_key']
    STORE_ID = config['store_id']
    
    url = "https://app.orderdesk.me/api/v2/inventory-items"
    headers = {
        "ORDERDESK-STORE-ID": STORE_ID,
        "ORDERDESK-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Get print_sku from csv based on Color and Size from wp product
    print_sku = get_orderdesk_print_sku(product['color'], product['size'])

    # Get the DropBox URL for artwork from user
    print_url = None
    while (print_url == None):
        print_url = input("DropBox image URL for " + product['sku'])

    # Print location is always center unless it's the propco logo t-shirt
    if ("logo" in product['sku']):
        print_location = "leftchest"
    else:
        print_location = "front"

    data = {
        "name": product['name'],
        "code": product['sku'],
        "price": product['price'],
        "stock": product['weight'],
        "metadata": {
            "print_sku": print_sku,
            "print_url": print_url,
            "print_location": print_location
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['inventory_item']
    else:
        print(f"Error creating inventory item: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    items = get_inventory_items()
    print(f"Retrieved {len(items)} inventory items")