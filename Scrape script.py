from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import re

# Define the start and end IDs
start_id = 2
end_id = 100000  # Adjust as per your need

# Define the filename with full path
filename = os.path.join(os.getcwd(), 'extracted_datatest.csv')
print("Current Working Directory:", os.getcwd())
print("File will be saved to:", filename)

# Function to create a new WebDriver instance
def create_driver():
    return webdriver.Chrome()

# Initialize the driver
driver = create_driver()

def get_page_data(url, driver):
    # Initialize a dictionary to hold the extracted data for each field
    extracted_data = {
        'Address': '',
        'Ejendomsværdi': '',
        'Grundværdi': ''
    }
    try:
        driver.get(url)
        
        # Wait for the h1 tag to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        
        # Extract <h1> text which contains the address
        h1_tag = soup.find('h1')
        if h1_tag:
            h1_text = h1_tag.get_text(strip=True)
        else:
            h1_text = 'No H1 tag found'
        
        extracted_data['Address'] = h1_text

        # Extract terms and their corresponding values
        dt_tags = soup.find_all('dt')
        for dt in dt_tags:
            term = dt.get_text(strip=True)
            dd = dt.find_next_sibling('dd')  # Find the next <dd> sibling tag
            if dd:
                value_text = dd.get_text(strip=True)
                value = re.search(r'(\d+\.?\d*)', value_text).group()
                
                if 'Ejendomsværdi' in term:
                    extracted_data['Ejendomsværdi'] = value
                elif 'Grundværdi' in term:
                    extracted_data['Grundværdi'] = value
    
    except Exception as e:
        print(f"Error processing page {url}: {e}")

    return extracted_data

# Main loop with retry mechanism
try:
    for i in range(start_id, end_id + 1):
        url = f'https://www.vurderingsportalen.dk/ejerbolig/vurdering/foreloebige-vurderinger-ejendomssoegning/?id={i}'
        
        for attempt in range(3):  # Retry up to 3 times
            try:
                page_data = get_page_data(url, driver)
                break
            except Exception as e:
                print(f"Retry {attempt + 1} for ID {i} failed: {e}")
                if attempt == 2:  # If the third attempt fails, log and continue
                    print(f"Skipping ID {i} after 3 failed attempts.")
                    page_data = None
                    break
                time.sleep(5)  # Wait before retrying
        
        if page_data:
            df = pd.DataFrame([page_data])  # Create a DataFrame from a dictionary

            with open(filename, 'a', newline='', encoding='utf-8') as f:
                df.to_csv(f, index=False, header=f.tell()==0)
            print(f"Data for ID {i} written to file.")

        # Take a break after every 10 requests
        if (i - start_id + 1) % 10 == 0:
            print(f"Taking a break after processing {i - start_id + 1} pages.")
            time.sleep(4)  # Adjust the sleep time as needed
    
finally:
    driver.quit()