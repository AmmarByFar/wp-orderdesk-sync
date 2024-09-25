import os
from dotenv import load_dotenv
from src.wordpress import get_products
from src.orderdesk import get_inventory_items, create_inventory_item

def main():
    load_dotenv()
    print("Getting products...")
    # Get products from WordPress
    wordpress_products = get_products()

    # Get inventory items from OrderDesk
    orderdesk_inventory = get_inventory_items()

    # print("# WordPress Items:")
    # for p in wordpress_products:
    #     if p['sku'] != None:
    #         print(p['name'], p['sku'], p['size'], p['price'], p['weight'])

    # print("# OrderDesk Items:")
    # for i in orderdesk_inventory:
    #     print(i['name'], i['code'])

    # Create a set of SKUs from OrderDesk inventory for efficient lookup
    orderdesk_skus = set(item['code'] for item in orderdesk_inventory)

    # Find products in WordPress that don't exist in OrderDesk
    new_products = [product for product in wordpress_products if product['sku'] not in orderdesk_skus]

    # Create new inventory items in OrderDesk
    for product in new_products:
        create_inventory_item(product)
        print(f"Created new inventory item in OrderDesk: (SKU: {product['sku']})")

    print(f"Sync complete. {len(new_products)} new items added to OrderDesk inventory.")

if __name__ == "__main__":
    main()