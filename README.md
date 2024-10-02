# WordPress-OrderDesk Inventory Sync

This Python script synchronizes product inventory between WordPress (WooCommerce) and OrderDesk + FulfillEngine. It fetches products from WordPress, compares them with the existing inventory in OrderDesk, and creates new inventory items in OrderDesk for products that don't exist there yet.

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library
- WooCommerce setup with products having Color and Size attributes
- OrderDesk account and API credentials
- CSV file with print SKUs (named `bc3001-skus.csv`)

## Setup

1. Clone this repository to your local machine.
2. Install the required Python packages:
   ```
   pip install requests python-dotenv
   ```
3. Create a `.env` file in the root directory with the following content:
   ```
   ORDERDESK_API_KEY=your_api_key_here
   ORDERDESK_STORE_ID=your_store_id_here
   WORDPRESS_SITE_URL=your_wordpress_site_url
   WORDPRESS_CONSUMER_KEY=your_consumer_key
   WORDPRESS_CONSUMER_SECRET=your_consumer_secret

   ```
4. Ensure the `bc3001-skus.csv` file is present in the `.../path/wp-orderdesk-sync/` directory (or update the path in the `get_orderdesk_print_sku` function).

## Usage

Run the script using Python:

```
python main.py
```

The script will:
1. Fetch products from WordPress
2. Fetch inventory items from OrderDesk
3. Compare the two and identify new products
4. For each new product:
   - Prompt you to enter a DropBox image URL
   - Create a new inventory item in OrderDesk

## Functions

- `main()`: The main function that orchestrates the synchronization process.
- `get_products()`: Fetches products from WordPress (implementation not shown in the provided code).
- `get_inventory_items()`: Retrieves inventory items from OrderDesk.
- `get_orderdesk_print_sku(color, size)`: Looks up the print SKU from the CSV file based on color and size.
- `create_inventory_item(product)`: Creates a new inventory item in OrderDesk.

## Notes

- The script assumes that the WordPress products have 'color' and 'size' attributes set, which are used to correlate with the correct SKU from the CSV file.
- For products with "logo" in the SKU, the print location is set to "leftchest"; otherwise, it's set to "front".
- The script will prompt for a DropBox image URL for each new product being added to OrderDesk.
- Stock levels are set based on the 'weight' field of the WordPress product (this might need adjustment based on your specific setup).

## Error Handling

The script includes basic error handling for API requests. If an error occurs during the API calls, it will print the error status code and response text.

## Customization

You may need to adjust the script based on your specific WordPress setup, OrderDesk configuration, and CSV file structure. Pay particular attention to the product attribute mapping and the CSV file path.