import requests
import csv
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed for HTTPS requests
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Define the path to your CSV file here
csv_file_path = ''

# Define the path to where you want to save the content
save_path = ''
new_csv_file_path = 'open_80_443_RESULTS.csv'  # Use the actual path for the new CSV file

# Function to clean up column headers
def clean_headers(headers):
    return [h.strip() for h in headers]

updated_rows = []

# Read the CSV file
with open(csv_file_path, mode='r', newline='', encoding='utf-8-sig') as file:
    # Use a DictReader to easily access columns
    csv_reader = csv.DictReader(file)
    # Store the current headers
    headers = csv_reader.fieldnames

    # Go through each row and attempt to fetch content
    for row in csv_reader:
        # Determine the protocol and construct the URL
        protocol = 'https' if row['Port'].strip() == '443' else 'http'
        url = f"{protocol}://{row['IP'].strip()}"

        try:
            # Fetch the content
            response = requests.get(url, verify=False, timeout=10)
            if response.status_code == 200:
                # If successful, update the row with fetched status
                row['Content_Fetched'] = 'Yes'
            else:
                row['Content_Fetched'] = 'No'
        except requests.exceptions.RequestException:
            # If there's an error, update the row with not fetched status
            row['Content_Fetched'] = 'No'

        # Add the updated row to the list
        print("completed 1")
        updated_rows.append(row)

    # Add the new column to the headers if it doesn't already exist
    if 'Content_Fetched' not in headers:
        headers.append('Content_Fetched')

# Write the updated data back into a new CSV file
with open(csv_file_path.replace('.csv', '_updated.csv'), 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(updated_rows)