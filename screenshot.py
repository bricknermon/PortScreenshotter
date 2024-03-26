import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from openpyxl import Workbook
from urllib3.exceptions import InsecureRequestWarning
import os
import time  # To add delay if needed
from PIL import Image as PILImage 
from openpyxl.drawing.image import Image

# Suppress only the single InsecureRequestWarning from urllib3 needed for HTTPS requests
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Define the path to your CSV file here
csv_file_path = ''

options = Options()
options.headless = True
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
options.add_argument('--allow-insecure-localhost')  # Allow insecure localhost
driver = webdriver.Chrome(options=options)

# Initialize Excel workbook
wb = Workbook()
ws = wb.active

# Create headers for the Excel file
ws.append(['IP', 'Host', 'OS', 'Proto', 'Port', 'Service', 'Product', 'Screenshot'])

# Read the CSV file
with open(csv_file_path, mode='r', newline='', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        if row['Content_Fetched'].strip().lower() == 'yes':
            try:
                # Determine the protocol and construct the URL
                protocol = 'https' if row['Port'].strip() == '443' else 'http'
                url = f"{protocol}://{row['IP'].strip()}"

                # Take a screenshot using Selenium
                driver.get(url)
                screenshot_file_name = f"screenshot_{row['IP'].strip()}.png"
                driver.save_screenshot(screenshot_file_name)
                
                # Append row data into the workbook
                ws.append([
                    row['IP'], row['Host'], row['OS'], row['Proto'],
                    row['Port'], row['Service'], row['Product']
                ])
                
                # Open the screenshot with PIL to ensure it's in memory
                pil_img = PILImage.open(screenshot_file_name)
                pil_img.save(screenshot_file_name)  # Save the image back if needed
                
                # Convert PIL image to a BytesIO object
                from io import BytesIO
                img_byte_array = BytesIO()
                pil_img.save(img_byte_array, format=pil_img.format)
                
                # Get the row number to place the image
                row_number = ws.max_row
                
                time.sleep(2)
                
                # Create an Image object for openpyxl
                openpyxl_img = Image(img_byte_array)
                openpyxl_img.anchor = f'H{row_number}'  # Assuming 'H' column is for screenshots
                ws.add_image(openpyxl_img)
                
                # Optionally, remove the screenshot file after adding it to the workbook
                #os.remove(screenshot_file_name)
            except WebDriverException as e:
                print(f"An error occurred while taking screenshot of {url}: {e}")
                ws.append([
                    row['IP'], row['Host'], row['OS'], row['Proto'],
                    row['Port'], row['Service'], row['Product'],
                    'Error taking screenshot'
                ])
        else:
            # Insert row data without a screenshot
            ws.append([
                row['IP'], row['Host'], row['OS'], row['Proto'],
                row['Port'], row['Service'], row['Product'],
                'Content not fetched'
            ])

# Try saving the workbook
try:
    wb.save('open_80_443_scan_results.xlsx')
except Exception as e:
    print(f"An error occurred while saving the workbook: {e}")

# Quit the Selenium WebDriver session
driver.quit()