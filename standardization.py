"""
Author: Nathan Malamud
Date: Thursday, Oct 17th 2024

Goal: Find instances of known names to standardize and
fill first, second, last name columns with standard values.

Dependency: Audra's string parsing code (comparison.py)

Chat-GPT4 log:
  https://chatgpt.com/share/671571e6-5924-8012-89c1-c888afc546ef
"""

# Import necessary libraries
import pandas as pd
import regex as re
import dplython as dplyr
from dplython import (DplyFrame, X, sift)

# ... (previous code for loading and preparing data)

from parsing import tokenize, standardize, compare_names

# Helper function to open Excel files as DataFrames
def open_excel(file, header=0):
    return DplyFrame(pd.read_excel(file, header=header))

# Open agents dataframe and organizations
data = open_excel('./Names/Agents Download - Wed Oct 16 2024.xlsx')

# Rename column names for easy of indexing
original_columns = data.columns.copy()
data.columns = ['GUID', 'first', 'middle', 'last']

# Strip all trailing whitespace from text
data = data >> dplyr.mutate(first=X['first'].str.strip(),
                            middle=X['middle'].str.strip(),
                            last=X['last'].str.strip())
                            
# Replace "NaN" string values with NA
data = data >> dplyr.mutate(first=X['first'].replace('NaN', pd.NA),
                            middle=X['middle'].replace('NaN', pd.NA),
                            last=X['last'].replace('NaN', pd.NA))

# Create 'Combined Name' by concatenating first, middle, and last names
data['combined'] = data[['first', 'middle', 'last']].fillna('').agg(' '.join, axis=1).str.strip()

# Define patterns for filtering out exceptional cases
nan_pattern = r'^\s*$'  # Matches empty strings
length_pattern = r'^[^ ]{1,3}$'  # Matches 1 to 3 characters long strings
num_pattern = r'\d'  # Matches strings that contain numbers
anon_pattern = r'anon|anonymous|unnamed|unknown|unidentified|name withheld|witheld|nobody|no name|noname|unattributed'
student_pattern = r'student' # Matches "student", "students", or "student of"

# Combine organization keywords into one big regex pattern
organization_keys = [
    # Education and Research
    "academy", "college", "class", "department", "faculty", "institute", "laboratory", "media",
    "network", "research", "school", "station", "students", "university", "ubc",
    
    # Government and Public Agencies
    "agency", "council", "federal", "judicial", "ministry", "municipal", "office", 
    "provincial", "state", 
    
    # Health and Medical
    "clinic", "health", "hospital", "medical", "pharmacy",
    
    # Legal and Financial
    "attorneys", "capital", "finance", "fund", "insurance", "investment", "legal", 
    
    # Technology and Digital
    "center", "digital", "hardware", "software", "solutions", "systems", "technology", 
    
    # Environmental and Conservation
    "alliance", "association", "biology", "coalition", "conservancy", "environmental", 
    "foundation", "garden", "group", "nature", "plants", "society", "wildlife", "working",
    
    # Business and Commerce
    "boutique", "commerce", "company", "firm", "holdings", "incorporated", "logistics",
    "market", "members", "organization", "trading",
    
    # Logistics and Transport
    "assurance", "maritime", "shipping", "transit",
    
    # Regional Locations
    "california", "oregon", "washington"
]

organization_pattern = '|'.join(organization_keys)

# Filter out unwanted rows (weird and special cases)
data_filtered = data >> sift(
    ~(X['first'].str.match(nan_pattern, na=False) & 
     X['middle'].str.match(nan_pattern, na=False) & 
     X['last'].str.match(nan_pattern, na=False)) & 
    ~X['combined'].str.match(length_pattern, na=False) &
    ~X['combined'].str.contains(num_pattern, na=False) &
    ~X['combined'].str.contains(anon_pattern, na=False, flags=re.IGNORECASE) &
    ~X['combined'].str.contains(student_pattern, na=False, flags=re.IGNORECASE) &
    ~X['combined'].str.contains(organization_pattern, na=False, flags=re.IGNORECASE)
)

# Additional filtering for multiple names, remove these from dataframe
data_multiple = data_filtered >> sift(X['combined'].str.contains(r'\band\b|\bor\b|\band/or\b|,', na=False))
data_filtered = data_filtered >> sift(~X['combined'].str.contains(r'\band\b|\bor\b|\band/or\b|,', na=False))

# - - - - - - - - - - -
# If we have a list of standard names and known exceptions... we can just build separate
# routines that go through the data and apply the standardization rules unique to each person.

# Assuming we have a list of names formatted as [first] [initial] [last]
# Let's strip unneccesary whitespaces by splitting words and recombining
# This will help us match names more accurately
data_filtered['combined_tokens'] = data_filtered['combined'].apply(lambda x: ' '.join(tokenize(x)))

from classifier import *

# Find all instances of all standard names
# Apply the function to the combined column and create a boolean mask
# Extract data that matches any of standard names
# Create a dispatch table mapping standard names to their respective classification functions
dispatch = {
    "Frank Lomer": match_frank_lomer,
    "Vladimir J. Krajina": match_vladimir_krajina,
    "Thomas M.C. Taylor": match_thomas_taylor,
    "John W. Eastham": match_john_eastham,
    "Katherine I. Beamish": match_katherine_beamish,
    "Gerald B. Straley": match_gerald_straley,
    "Vernon C. Brink": match_vernon_brink,
    "John Davidson": match_john_davidson,
    "Adam F. Szczawinski": match_adam_szczawinski,
    "James A. Calder": match_james_calder,
    "Freek Vrugtman": match_freek_vrugtman,
    "William Copeland McCalla": match_william_mccalla,
    "Jim J. Pojar": match_jim_pojar,
    "Roy L. Taylor": match_roy_taylor,
    "Bruce A. Bennett": match_bruce_bennett,
    "Beryl C. Zhuang": match_beryl_zhuang,
    "Trevor Goward": match_trevor_goward,
    "Jeffery M. Saarela": match_jeffery_saarela,
    "Terry T. McIntosh": match_terry_mcintosh,
    "William J. Cody": match_william_cody,
    "Fred Fodor": match_fred_fodor,
    "Charles E. Beil": match_charles_beil,
    "Curtis R. Bjork": match_curtis_bjork,
    "Jamie D. Fenneman": match_jamie_fenneman,
    "Erin R. Manton": match_erin_manton,
    "Adolf Ceska": match_adolf_ceska,
    "Oluna Ceska": match_oluna_ceska,
    "L.E. Taylor": match_le_taylor,
    "John Pinder-Moss": match_john_pinder_moss,
    "Wilfred Schofield": match_wilfred_schofield,
    "Corinne J. Selby": match_corinne_selby,
    "D.B.O. Savile": match_db_o_savile,
    "Eli Wilson": match_eli_wilson,
    "Linda Jennings": match_linda_jennings,
    "Quentin Cronk": match_quentin_cronk
}

# Function to classify names and return the standard name if matched
def classify_name(row):
    name = row['combined_tokens']
    
    for standard_name, match_function in dispatch.items():
        if match_function(name):
            return standard_name
            
    return None  # Return None if no match found

# Apply the classify_name function to each row
data_filtered['standard'] = data_filtered.apply(classify_name, axis=1)

# List to store mismatched entries
mismatched_entries = []

# Iterate through the DataFrame to compare combined names with standard names
for index, row in data_filtered.iterrows():
    combined_name = row['combined']
    standard_name = row['standard']
    
    if combined_name is None or standard_name is None:
        continue
    
    # Check if the combined name does not match the standard name
    if not compare_names(combined_name, standard_name, threshold=0.75):
        mismatched_entries.append({
            'GUID': row['GUID'],
            'combined': combined_name,
            'standard': standard_name,
            'match': False  # Indicate that this is a mismatch
        })

# Convert the mismatched entries into a DataFrame
mismatched_data = pd.DataFrame(mismatched_entries)

# Get all instances of Jim J. Pojar using match function
# Filter for all instances of 'Jim J. Pojar' using a filter or match function
# Get the matching function for 'Jim J. Pojar' from the dispatch table
frank_lomer = data_filtered >> sift(X['standard'] == 'Frank Lomer')
vladimir_krajina = data_filtered >> sift(X['standard'] == 'Vladimir J. Krajina')
thomas_taylor = data_filtered >> sift(X['standard'] == 'Thomas M.C. Taylor')
john_eastham = data_filtered >> sift(X['standard'] == 'John W. Eastham')
katherine_beamish = data_filtered >> sift(X['standard'] == 'Katherine I. Beamish')
gerald_straley = data_filtered >> sift(X['standard'] == 'Gerald B. Straley')
vernon_brink = data_filtered >> sift(X['standard'] == 'Vernon C. Brink')
john_davidson = data_filtered >> sift(X['standard'] == 'John Davidson')
adam_szczawinski = data_filtered >> sift(X['standard'] == 'Adam F. Szczawinski')
james_calder = data_filtered >> sift(X['standard'] == 'James A. Calder')
freek_vrugtman = data_filtered >> sift(X['standard'] == 'Freek Vrugtman')
william_mccalla = data_filtered >> sift(X['standard'] == 'William Copeland McCalla')
jim_pojar = data_filtered >> sift(X['standard'] == 'Jim J. Pojar')
roy_taylor = data_filtered >> sift(X['standard'] == 'Roy L. Taylor')
bruce_bennett = data_filtered >> sift(X['standard'] == 'Bruce A. Bennett')
beryl_zhuang = data_filtered >> sift(X['standard'] == 'Beryl C. Zhuang')
trevor_goward = data_filtered >> sift(X['standard'] == 'Trevor Goward')
jeffery_saarela = data_filtered >> sift(X['standard'] == 'Jeffery M. Saarela')
terry_mcintosh = data_filtered >> sift(X['standard'] == 'Terry T. McIntosh')
william_cody = data_filtered >> sift(X['standard'] == 'William J. Cody')
fred_fodor = data_filtered >> sift(X['standard'] == 'Fred Fodor')
charles_beil = data_filtered >> sift(X['standard'] == 'Charles E. Beil')
curtis_bjork = data_filtered >> sift(X['standard'] == 'Curtis R. Bjork')
jamie_fenneman = data_filtered >> sift(X['standard'] == 'Jamie D. Fenneman')
erin_manton = data_filtered >> sift(X['standard'] == 'Erin R. Manton')
adolf_ceska = data_filtered >> sift(X['standard'] == 'Adolf Ceska')
oluna_ceska = data_filtered >> sift(X['standard'] == 'Oluna Ceska')
le_taylor = data_filtered >> sift(X['standard'] == 'L.E. Taylor')
john_pinder_moss = data_filtered >> sift(X['standard'] == 'John Pinder-Moss')
wilfred_schofield = data_filtered >> sift(X['standard'] == 'Wilfred Schofield')
corinne_selby = data_filtered >> sift(X['standard'] == 'Corinne J. Selby')
db_o_savile = data_filtered >> sift(X['standard'] == 'D.B.O. Savile')
eli_wilson = data_filtered >> sift(X['standard'] == 'Eli Wilson')
linda_jennings = data_filtered >> sift(X['standard'] == 'Linda Jennings')
quentin_cronk = data_filtered >> sift(X['standard'] == 'Quentin Cronk')

# Final to_standardize dataframe
to_standardize = pd.concat([
    frank_lomer, vladimir_krajina, thomas_taylor, john_eastham, katherine_beamish,
    gerald_straley, vernon_brink, john_davidson, adam_szczawinski, james_calder,
    freek_vrugtman, william_mccalla, jim_pojar, roy_taylor, bruce_bennett,
    beryl_zhuang, trevor_goward, jeffery_saarela, terry_mcintosh, william_cody,
    fred_fodor, charles_beil, curtis_bjork, jamie_fenneman, erin_manton,
    adolf_ceska, oluna_ceska, le_taylor, john_pinder_moss, wilfred_schofield,
    corinne_selby, db_o_savile, eli_wilson, linda_jennings, quentin_cronk
])

# select only relevant columns
to_standardize = to_standardize[['GUID', 'first', 'middle', 'last', 'standard']]
to_standardize = to_standardize.rename(columns={
    'GUID': 'GUID', 
    'first': 'First.Name', 
    'middle': 'Middle.Name', 
    'last': 'Last.Name', 
    'standard': 'Standardized Name'
})
to_standardize.to_excel("to_standardize.xlsx", index=False)
