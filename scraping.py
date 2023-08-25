import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import csv

# Base URL of the website to scrape
base_url = "https://medicalsolution.com.tr/shop/"
# Total number of pages to scrape
total_pages = 13

# Create a directory to store images
if not os.path.exists("product_images"):
    os.makedirs("product_images")

# Create a CSV file to store the data
csv_filename = "product_data.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Product Name", "Product Price", "Product Description", "Image Filenames"])

    for page in range(1, total_pages + 1):
        # Construct the URL for the current page
        url = f"{base_url}/page/{page}/"
        
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find all product containers
            product_containers = soup.find_all("li", class_="product")
            
            # Loop through each product container
            for container in product_containers:
                # Extract product name
                product_name = container.find("h2", class_="woocommerce-loop-product__title").text.strip()
                
                # Extract product price
                product_price = container.find("span", class_="woocommerce-Price-amount").text.strip()
                
                # Extract product image URL
                image_url = container.find("img", class_="attachment-woocommerce_thumbnail")["src"]
                full_image_url = urljoin(url, image_url)
                
                # Construct the URL for the individual product page
                product_page_url = urljoin(url, container.find("a")["href"])
                
                # Send an HTTP GET request to the product page
                product_page_response = requests.get(product_page_url)
                
                if product_page_response.status_code == 200:
                    # Parse the individual product page
                    product_page_soup = BeautifulSoup(product_page_response.content, "html.parser")
                    
                    # Extract product description
                    product_description = product_page_soup.find("div", class_="woocommerce-Tabs-panel--description").text.strip()
                    
                    # Extract additional product images
                    additional_images_div = product_page_soup.find("figure", class_="woocommerce-product-gallery__wrapper")
                    additional_image_urls = [urljoin(url, img["src"]) for img in additional_images_div.find_all("img")]
                    
                    # Download and save additional images
                    additional_image_filenames = []
                    for i, image_url in enumerate(additional_image_urls, start=1):
                        image_response = requests.get(image_url)
                        image_filename = os.path.join("product_images", f"{product_name}_image_{i}.jpg")
                        with open(image_filename, "wb") as image_file:
                            image_file.write(image_response.content)
                        additional_image_filenames.append(image_filename)
                    
                    # Write data to the CSV file
                    csv_writer.writerow([product_name, product_price, product_description, ", ".join(additional_image_filenames)])
                    
                    # Print the scraped data
                    print("Product Name:", product_name)
                    print("Product Price:", product_price)
                    print("Product Description:", product_description)
                    print("Additional Image Filenames:", ", ".join(additional_image_filenames))
                    print("=" * 30)
                else:
                    print("Failed to retrieve the product page. Status code:", product_page_response.status_code)
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)












# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import csv

# # Base URL of the website to scrape
# base_url = "https://medicalsolution.com.tr/shop"
# # Total number of pages to scrape
# total_pages = 13

# # Create a directory to store images
# if not os.path.exists("product_images"):
#     os.makedirs("product_images")

# # Create a CSV file to store the data
# csv_filename = "product_data.csv"
# with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(["Product Name", "Product Price", "Image Filename"])

#     for page in range(1, total_pages + 1):
#         # Construct the URL for the current page
#         url = f"{base_url}/page/{page}/"
        
#         # Send an HTTP GET request to the URL
#         response = requests.get(url)
        
#         # Check if the request was successful
#         if response.status_code == 200:
#             # Parse the HTML content using BeautifulSoup
#             soup = BeautifulSoup(response.content, "html.parser")
            
#             # Find all product containers
#             product_containers = soup.find_all("li", class_="product")
            
#             # Loop through each product container
#             for container in product_containers:
#                 # Extract product name
#                 product_name = container.find("h2", class_="woocommerce-loop-product__title").text.strip()
                
#                 # Extract product price
#                 product_price = container.find("span", class_="woocommerce-Price-amount").text.strip()
                
#                 # Extract product image URL
#                 image_url = container.find("img", class_="attachment-woocommerce_thumbnail")["src"]
#                 full_image_url = urljoin(url, image_url)
                
#                 # Send an HTTP GET request for the image
#                 image_response = requests.get(full_image_url)
                
#                 # Save the image to the product_images directory
#                 image_filename = os.path.join("product_images", f"{product_name}.jpg")
#                 with open(image_filename, "wb") as image_file:
#                     image_file.write(image_response.content)
                
#                 # Write data to the CSV file
#                 csv_writer.writerow([product_name, product_price, image_filename])
                
#                 # Print the scraped data
#                 print("Product Name:", product_name)
#                 print("Product Price:", product_price)
#                 print("Image Filename:", image_filename)
#                 print("=" * 30)
#         else:
#             print("Failed to retrieve the webpage. Status code:", response.status_code)
