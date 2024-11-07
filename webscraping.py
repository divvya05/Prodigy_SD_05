import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_jumia_products(url, num_pages=1):
    """
    Scrapes product information (name, price, rating) from Jumia's search result pages.
    
    Parameters:
        url (str): The base URL for the search page (including the search query) on Jumia.
        num_pages (int): Number of pages to scrape. Defaults to 1.

    Returns:
        list: A list of dictionaries, each containing 'Name', 'Price', and 'Rating' for a product.
    """
    
    # Initialize an empty list to store product data
    products = []
    
    # Define headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    
    # Loop through the specified number of pages
    for page in range(1, num_pages + 1):
        # Send a GET request to the URL for each page, adding pagination query
        response = requests.get(f"{url}&page={page}", headers=headers)
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all product elements on the page
        product_elements = soup.find_all('article', class_='prd _fb col c-prd')
        
        # Iterate over each product found on the page
        for product in product_elements:
            try:
                # Extract product name
                name = product.find('h3', class_='name').get_text(strip=True)
                
                # Extract product price
                price = product.find('div', class_='prc').get_text(strip=True)
                
                # Extract product rating if available, else assign 'No Rating'
                rating = product.find('div', class_='stars _s').get_text(strip=True) if product.find('div', class_='stars _s') else 'No Rating'
                
                # Store product details in a dictionary
                product_data = {
                    'Name': name,
                    'Price': price,
                    'Rating': rating
                }
                
                # Append product data to the list of products
                products.append(product_data)
            except Exception as e:
                print(f"Error extracting data for a product: {e}")
        
        # Pause briefly to avoid overwhelming the server (good practice in scraping)
        time.sleep(1)
    
    # Return the complete list of scraped product data
    return products

def save_to_csv(data, filename='jumia_products.csv'):
    """
    Saves a list of product dictionaries to a CSV file.
    
    Parameters:
        data (list): List of dictionaries with product details (name, price, rating).
        filename (str): The filename for the CSV file. Defaults to 'jumia_products.csv'.
    """
    
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Save DataFrame to a CSV file
    df.to_csv(filename, index=False)
    
    print(f"Data saved to {filename}")

# Main usage example
# Replace with a valid Jumia URL for the search category of interest
jumia_url = 'https://www.jumia.com.ng/catalog/?q=smartphones'  # Example: search results for 'smartphones'

# Call the scraping function for 3 pages of search results as a test
data = scrape_jumia_products(jumia_url, num_pages=3)

# Save the scraped data to a CSV file
save_to_csv(data)