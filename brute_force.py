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
import numpy as np
import regex as re
import dplython as dplyr
from dplython import (DplyFrame, X, sift, mutate)

from compare_names import tokenize, standardize, compare_names

# Helper function to open Excel files as DataFrames
def open_excel(file, header=0):
    return DplyFrame(pd.read_excel(file, header=header))
  
# Tokenize names: clean, split, and remove stop words (and suffixes)
def tokenize(name):
    clean_name = name.lower().strip()
    tokens = re.split(r'[\s.?,{\[\(]+', clean_name) 
    return [t for t in tokens if t not in ['and', 'or', 'is', 'for', '', 'mr', 'mrs', 'dr', 'drs', 'jr']]

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

# Define patterns for filtering and categorizing cases
nan_pattern = r'^\s*$'  # Matches empty strings
length_pattern = r'^[^ ]{1,5}$'  # Matches 1 to 5 characters long strings
num_pattern = r'\d'  # Matches strings that contain numbers
anon_pattern = r'anon|anonymous|unnamed|unknown|unidentified|name withheld|witheld|nobody|no name|noname|unattributed'

# Combine organization keywords into one regex pattern
organization_keys = [
    "academy", "college", "class", "department", "faculty", "institute", "laboratory", "media",
    "network", "research", "school", "station", "students", "university", "ubc",
    "agency", "council", "federal", "judicial", "ministry", "municipal", "office", 
    "provincial", "state", "clinic", "health", "hospital", "medical", "pharmacy",
    "attorneys", "capital", "finance", "fund", "insurance", "investment", "legal", 
    "center", "digital", "hardware", "software", "solutions", "systems", "technology", 
    "alliance", "association", "biology", "coalition", "conservancy", "environmental", 
    "foundation", "garden", "group", "nature", "plants", "society", "wildlife", "working",
    "boutique", "commerce", "company", "firm", "holdings", "incorporated", "logistics",
    "market", "members", "organization", "trading", "assurance", "maritime", "shipping", "transit",
    "california", "oregon", "washington"
]
organization_pattern = '|'.join(organization_keys)

# Fill 'standard' column based on conditions
# Define the conditions for each category
conditions = [
    (data['first'].str.match(nan_pattern, na=False) & 
     data['middle'].str.match(nan_pattern, na=False) & 
     data['last'].str.match(nan_pattern, na=False)) | 
    data['combined'].str.contains(anon_pattern, na=False, flags=re.IGNORECASE),
    data['combined'].str.contains(organization_pattern, na=False, flags=re.IGNORECASE),
    data['combined'].str.contains(num_pattern, na=False),
    data['combined'].str.match(length_pattern, na=False)
]

# Define the corresponding values for each category
choices = [
    "Anonymous",
    "Organization",
    "Contains Number",
    "Short Name"
]

# Apply np.select to create 'standard' column based on conditions
data = data >> mutate(
    standard=np.select(conditions, choices, default=pd.NA)
)

# The resulting dataframe `data` now contains a 'standard' column with categorized entries.

# - - - - - - - - - - -
# If we have a list of standard names and known exceptions... we can just build separate
# routines that go through the data and apply the standardization rules unique to each person.

# Assuming we have a list of names formatted as [first] [initial] [last]
# Let's strip unneccesary whitespaces by splitting words and recombining
# This will help us match names more accurately
data['combined_tokens'] = data['combined'].apply(lambda x: ' '.join(tokenize(x)))

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
    "Quentin Cronk": match_quentin_cronk,
    # TODO: input new names
    "William Randolph Taylor" : match_william_randolph_taylor,
    "F.J.R. Taylor" : match_fj_r_taylor,
    "Sandra C. Lindstrom" : match_sandra_c_lindstrom,
    "Stephen S. Talbot" : match_stephen_s_talbot,
    "J.C. Oliveira" : match_jc_oliveira,
    "J.L. Celistino" : match_jl_celistino,
    "Stephen J. Oliver" : match_stephen_j_oliver,
    # For students of people
    "Student" : match_student
}

# Function to classify names and return the standard name if matched
def classify_name(row):
    name = row['combined_tokens']
    
    for standard_name, match_function in dispatch.items():
        if match_function(name):
            return standard_name
            
    return row['standard']  # Return default if no match found

# Apply the classify_name function to each row
data['standard'] = data.apply(classify_name, axis=1)

# - - - - - - - - - - - - 
# Test Cases
frank_lomer = data >> sift(X['standard'] == 'Frank Lomer')
vladimir_krajina = data >> sift(X['standard'] == 'Vladimir J. Krajina')
thomas_taylor = data >> sift(X['standard'] == 'Thomas M.C. Taylor')
john_eastham = data >> sift(X['standard'] == 'John W. Eastham')
katherine_beamish = data >> sift(X['standard'] == 'Katherine I. Beamish')
gerald_straley = data >> sift(X['standard'] == 'Gerald B. Straley')
vernon_brink = data >> sift(X['standard'] == 'Vernon C. Brink')
john_davidson = data >> sift(X['standard'] == 'John Davidson')
adam_szczawinski = data >> sift(X['standard'] == 'Adam F. Szczawinski')
james_calder = data >> sift(X['standard'] == 'James A. Calder')
freek_vrugtman = data >> sift(X['standard'] == 'Freek Vrugtman')
william_mccalla = data >> sift(X['standard'] == 'William Copeland McCalla')
jim_pojar = data >> sift(X['standard'] == 'Jim J. Pojar')
roy_taylor = data >> sift(X['standard'] == 'Roy L. Taylor')
bruce_bennett = data >> sift(X['standard'] == 'Bruce A. Bennett')
beryl_zhuang = data >> sift(X['standard'] == 'Beryl C. Zhuang')
trevor_goward = data >> sift(X['standard'] == 'Trevor Goward')
jeffery_saarela = data >> sift(X['standard'] == 'Jeffery M. Saarela')
terry_mcintosh = data >> sift(X['standard'] == 'Terry T. McIntosh')
william_cody = data >> sift(X['standard'] == 'William J. Cody')
fred_fodor = data >> sift(X['standard'] == 'Fred Fodor')
charles_beil = data >> sift(X['standard'] == 'Charles E. Beil')
curtis_bjork = data >> sift(X['standard'] == 'Curtis R. Bjork')
jamie_fenneman = data >> sift(X['standard'] == 'Jamie D. Fenneman')
erin_manton = data >> sift(X['standard'] == 'Erin R. Manton')
adolf_ceska = data >> sift(X['standard'] == 'Adolf Ceska')
oluna_ceska = data >> sift(X['standard'] == 'Oluna Ceska')
le_taylor = data >> sift(X['standard'] == 'L.E. Taylor')
john_pinder_moss = data >> sift(X['standard'] == 'John Pinder-Moss')
wilfred_schofield = data >> sift(X['standard'] == 'Wilfred Schofield')
corinne_selby = data >> sift(X['standard'] == 'Corinne J. Selby')
db_o_savile = data >> sift(X['standard'] == 'D.B.O. Savile')
eli_wilson = data >> sift(X['standard'] == 'Eli Wilson')
linda_jennings = data >> sift(X['standard'] == 'Linda Jennings')
quentin_cronk = data >> sift(X['standard'] == 'Quentin Cronk')
william_randolph_taylor = data >> sift(X['standard'] == 'William Randolph Taylor')
fj_r_taylor = data >> sift(X['standard'] == 'F.J.R. Taylor')
sandra_c_lindstrom = data >> sift(X['standard'] == 'Sandra C. Lindstrom')
stephen_s_talbot = data >> sift(X['standard'] == 'Stephen S. Talbot')
jc_oliveira = data >> sift(X['standard'] == 'J.C. Oliveira')
jl_celestino = data >> sift(X['standard'] == 'J.L. Celistino')
stephen_j_oliver = data >> sift(X['standard'] == 'Stephen J. Oliver')

# Final to_standardize dataframe
to_standardize = pd.concat([
    frank_lomer, vladimir_krajina, thomas_taylor, john_eastham, katherine_beamish,
    gerald_straley, vernon_brink, john_davidson, adam_szczawinski, james_calder,
    freek_vrugtman, william_mccalla, jim_pojar, roy_taylor, bruce_bennett,
    beryl_zhuang, trevor_goward, jeffery_saarela, terry_mcintosh, william_cody,
    fred_fodor, charles_beil, curtis_bjork, jamie_fenneman, erin_manton,
    adolf_ceska, oluna_ceska, le_taylor, john_pinder_moss, wilfred_schofield,
    corinne_selby, db_o_savile, eli_wilson, linda_jennings, quentin_cronk,
    william_randolph_taylor, fj_r_taylor, sandra_c_lindstrom, stephen_s_talbot,
    jc_oliveira, jl_celestino, stephen_j_oliver
])

# List to store mismatched entries
mismatched_entries = []

# Iterate through the DataFrame to compare combined names with standard names
for index, row in to_standardize.iterrows():
    combined_name = row['combined']
    standard_name = row['standard']
    
    if combined_name is None or standard_name is None:
        continue
    
    # Check if the combined name does not match the standard name
    if not compare_names(combined_name, standard_name, threshold=0.5):
        mismatched_entries.append({
            'GUID': row['GUID'],
            'combined': combined_name,
            'standard': standard_name,
            'match': False  # Indicate that this is a mismatch
        })

# Convert the mismatched entries into a DataFrame
mismatched_data = pd.DataFrame(mismatched_entries)

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

# - - - - - - - - - - - -
# Next approach is to count remaining uncategorized names by alphabetical order
# This will help in identifying patterns and exceptions

# Ignore first, middle, last fields for now
# data_uncategorized = data >> \
#     sift(X['standard'].isna()) >> \
#     dplyr.select(X.GUID, X.combined, X.combined_tokens, X.standard)
#     
# # Assuming `tokenize` is a function that splits the name string into tokens
# # Extract last name with a check for empty tokens
# data_uncategorized['lastname'] = [
#     tokenize(name)[-1] if tokenize(name) else None for name in data_uncategorized['combined_tokens']
# ]
# 
# data_uncategorized['firstname'] = [
#     tokenize(name)[0] if tokenize(name) else None for name in data_uncategorized['combined_tokens']
# ]

# import matplotlib.pyplot as plt
# 
# # Group by the last name and count occurrences
# count_by_lastname = data_uncategorized.groupby('lastname').size().reset_index(name='count')
# 
# # Create a new column to group names with occurrences of 1 or 2 under "Other"
# count_by_lastname['lastname_grouped'] = count_by_lastname['lastname'].where(count_by_lastname['count'] > 5, 'Other')
# 
# # Re-aggregate the counts based on the new grouped names
# count_by_lastname_grouped = count_by_lastname.groupby('lastname_grouped')['count'].sum().reset_index()
# 
# # Plot a pie chart
# import matplotlib.pyplot as plt
# 
# plt.figure(figsize=(8, 8))
# plt.pie(count_by_lastname_grouped['count'], labels=count_by_lastname_grouped['lastname_grouped'], autopct='%1.1f%%', startangle=140)
# plt.title("Distribution of Entries by Last Name (Grouped)")
# plt.show()
# 
# # Group by the first name and count occurrences
# count_by_firstname = data_uncategorized.groupby('firstname').size().reset_index(name='count')
# 
# # Create a new column to group names with occurrences of 1 or 2 under "Other"
# count_by_firstname['firstname_grouped'] = count_by_firstname['firstname'].where(count_by_firstname['count'] > 20, 'Other')
# 
# # Re-aggregate the counts based on the new grouped names
# count_by_firstname_grouped = count_by_firstname.groupby('firstname_grouped')['count'].sum().reset_index()
# 
# # Count by first name
# import matplotlib.pyplot as plt
# 
# plt.figure(figsize=(8, 8))
# plt.pie(count_by_firstname_grouped['count'], labels=count_by_firstname_grouped['firstname_grouped'], autopct='%1.1f%%', startangle=140)
# plt.title("Distribution of Entries by First Name (Grouped)")
# plt.show()


