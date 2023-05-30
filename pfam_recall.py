import pandas as pd
import requests
from bs4 import BeautifulSoup



# Function to search for protein family names using the new website
def search_protein_family(pfam_code):
    url = f"https://www.ncbi.nlm.nih.gov/Structure/cdd/{pfam_code}"
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        protein_family_element = soup.find("span")
        
        if protein_family_element is not None:
            protein_family_name = protein_family_element.text.strip()
            return protein_family_name
        else:
            return "Not found"
    else:
        return "Not found"


# Read Excel file
df = pd.read_excel("input_file.xlsx", sheet_name="Sheet1")

# Specify the column name where PFam codes are stored
pfam_column = 'pfam code'

# Extract PFam codes from the specified column
pfam_codes = df[pfam_column].tolist()

# Search for protein family names for each PFam code
protein_family_names = []
for pfam_code in pfam_codes:
    protein_family_name = search_protein_family(pfam_code)
    protein_family_names.append(protein_family_name)

# Add protein family names to the DataFrame
df['Protein Family'] = protein_family_names

# Save the updated DataFrame to a new Excel file
df.to_excel("output_file.xlsx", index=False)
