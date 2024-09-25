import os
import requests
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'site_url': os.getenv('WORDPRESS_SITE_URL'),
        'consumer_key': os.getenv('WORDPRESS_CONSUMER_KEY'),
        'consumer_secret': os.getenv('WORDPRESS_CONSUMER_SECRET')
    }

def get_products():
    config = load_config()
    SITE_URL = config['site_url']
    CONSUMER_KEY = config['consumer_key']
    CONSUMER_SECRET = config['consumer_secret']

    url = f"{SITE_URL}/wp-json/wc/v3/products"
    
    params = {
        "per_page": 100,
    }
    
    products_list = []
    
    while url:
        response = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET)
        )
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            break
        
        products = response.json()
        
        for product in products:
            if product['type'] == 'variable':
                variations_url = f"{url}/{product['id']}/variations"
                variations_response = requests.get(
                    variations_url,
                    auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET)
                )
                
                if variations_response.status_code == 200:
                    variations = variations_response.json()
                    for variation in variations:
                        variation_data = {
                            'name': f"{product['name']} - {variation['attributes'][0]['option']}",
                            'sku': variation['sku'],
                            'price': variation['price'],
                            'weight': variation['weight'],
                            'color': next((attr['option'] for attr in variation['attributes'] if attr['name'].lower() == 'color'), None),
                            'size': next((attr['option'] for attr in variation['attributes'] if attr['name'].lower() == 'size'), None)
                        }
                        products_list.append(variation_data)
            else:
                product_data = {
                    'name': product['name'],
                    'sku': product['sku'],
                    'price': product['price'],
                    'weight': product['weight'],
                    'color': next((attr['options'][0] for attr in product['attributes'] if attr['name'].lower() == 'color'), None),
                    'size': next((attr['options'][0] for attr in product['attributes'] if attr['name'].lower() == 'size'), None)
                }
                products_list.append(product_data)
        
        # Check if there are more pages
        url = response.links.get('next', {}).get('url')
    
    return products_list

if __name__ == "__main__":
    products = get_products()
    print(json.dumps(products, indent=2))