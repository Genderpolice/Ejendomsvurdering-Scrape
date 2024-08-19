import pandas as pd
import re

# Load the dataset with the correct delimiter
filename = 'extracted_data3.csv'
df = pd.read_csv(filename, delimiter=';')

# Display the first few rows of the dataframe to understand its structure
print("Original DataFrame:")
print(df.head())

# Function to split the address into multiple components
def parse_address(address):
    if not isinstance(address, str):
        return pd.Series(['', '', '', ''])  # Return empty fields if the address is not a string
    
    # Define regex patterns for different parts of the address
    street_pattern = re.compile(r'^(.*?)(?=\d)')
    number_pattern = re.compile(r'(\d+[A-Za-z]?)')  # Updated to include the letter after the number
    floor_pattern = re.compile(r'(\d+\s*(TV|TH))', re.IGNORECASE)  # Floor includes number + TV or TH
    postal_city_pattern = re.compile(r'(\d{4}\s+.*)')

    # Find street name
    street_name_match = street_pattern.search(address)
    street_name = street_name_match.group(0).strip() if street_name_match else ''

    # Find number (the first number after the street name, including the letter if present)
    number_match = number_pattern.search(address)
    number = number_match.group(0).strip() if number_match else ''

    # Find floor (the part after the number that includes floor information and optional letter)
    floor_match = floor_pattern.search(address)
    floor = floor_match.group(0).strip() if floor_match else ''

    # Find postal code and city
    postal_city_match = postal_city_pattern.search(address)
    postal_city = postal_city_match.group(0).strip() if postal_city_match else ''

    return pd.Series([street_name, number, floor, postal_city])

# Apply the parse function to the 'Address' column and create new columns
df[['Street Name', 'Number', 'Floor', 'Postal City']] = df['Address'].apply(parse_address)

# Function to clean and convert numeric values, preserving trailing zeros
def clean_and_format_numeric(column):
    # Step 1: Force everything to a string and remove non-numeric characters except for comma and period
    column = column.astype(str).str.replace(r'[^\d,.-]', '', regex=True)
    
    # Step 2: Replace comma with period
    column = column.str.replace(',', '.')
    
    # Step 3: Convert to float, format to preserve trailing zeros, and keep as string
    return column.apply(lambda x: f"{float(x):.3f}" if pd.notnull(x) else '')

# Apply the cleaning and formatting function to both columns
df['Ejendomsværdi'] = clean_and_format_numeric(df['Ejendomsværdi'])
df['Grundværdi'] = clean_and_format_numeric(df['Grundværdi'])

# Drop the original Address column if no longer needed
df.drop(columns=['Address'], inplace=True)

# Save the transformed DataFrame to a new CSV with proper formatting
transformed_filename = 'transformed_data.csv'
df.to_csv(transformed_filename, index=False, float_format='%.3f')

print("Transformed DataFrame:")
print(df.head())