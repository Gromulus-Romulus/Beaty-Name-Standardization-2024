"""
Author: Nathan Malamud
Date: Thursday, Nov 2nd 2024

Goal: Find instances of known names to standardize and
fill first, second, last name columns with standard values.
"""

# Import Agents download (latest version)
import pandas as pd
import regex as re
import dplython as dplyr
from dplython import (DplyFrame, X, sift, mutate)

# Helper function to open Excel files as DataFrames
def open_excel(file, header=0):
    return DplyFrame(pd.read_excel(file, header=header))

# Tokenize names: clean, split, and remove stop words (and suffixes)
def tokenize(name):
    clean_name = name.lower().strip()
    tokens = re.split(r'[\s.?,{\[\(]+', clean_name) 
    return [t for t in tokens if t not in ['nan', 'and', 'or', 'is', 'for', '', 'mr', 'mrs', 'dr', 'drs', 'jr']]
  
# Open agents dataframe and organizations
data = open_excel('./Names/Agents Download - Wed Oct 16 2024.xlsx')

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
                            
data = data >> dplyr.mutate(first=X['first'].replace('nan', pd.NA),
                            middle=X['middle'].replace('nan', pd.NA),
                            last=X['last'].replace('nan', pd.NA))

# Combine "first" "middle" and "last" into "original"
data['original'] = data.apply(lambda x: f"{x['first']} {x['last']}" if pd.isna(x['middle']) 
                              else f"{x['first']} {x['middle']} {x['last']}", axis=1)

# Filter first middle and last out of dataframe
data = data.drop(columns=['first', 'middle', 'last'])

# Now, tokenize combined original string
data['tokenized'] = data['original'].apply(lambda x: ' '.join(tokenize(x)))

# Now add new first, middle, last columns populated with pd.NA
data['first'] = pd.NA
data['middle'] = pd.NA
data['last'] = pd.NA

# We're going to build a list of standard names
standards = []

# Filter out rows that are part of a group, class, or organization
organization_keys = [
    "academy", "college", "class", "classes", "department", "faculty", "institute", "laboratory", "media",
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
organizations = data[data['tokenized'].str.contains(organization_pattern, case=False)]
data = data[~data['tokenized'].str.contains(organization_pattern, case=False)]

# Filter out rows that are anonymous or empty
anon_pattern = r'anon|anonymous|unnamed|unknown|unidentified|name withheld|witheld|nobody|no name|noname|unattributed'
anon = data[data['tokenized'].str.contains(anon_pattern, case=False)]
data = data[~data['tokenized'].str.contains(anon_pattern, case=False)]

nan_pattern = r'^\s*$'
nan = data[data['tokenized'].str.contains(nan_pattern, case=False)]
data = data[~data['tokenized'].str.contains(nan_pattern, case=False)]

# Define regex patterns for finding names (~1200 do not match these cases)
first_m_last = re.compile(r'\b(\w[\w-]+)\s(\w)\s([\w-]+)\b')
f_m_last = re.compile(r'\b(\w)\s(\w)\s([\w-]+)\b')
first_last = re.compile(r'\b([\w-]+)\s([\w-]+)\b')

# Iterate through each row and apply the patterns
for i, row in data.iterrows():
    tokenized = row['tokenized']
    
    # Check for F M Last pattern
    if match := f_m_last.match(tokenized):
        first, middle, last = match.groups()
        data.at[i, 'first'] = f'{first.upper()}.'
        data.at[i, 'middle'] = f'{middle.upper()}.'
        data.at[i, 'last'] = last.capitalize()
        
    # Check for First Middle Last pattern
    elif match := first_m_last.match(tokenized):
        first, middle, last = match.groups()
        data.at[i, 'first'] = first.capitalize()
        data.at[i, 'middle'] = f'{middle.upper()}.'
        data.at[i, 'last'] = last.capitalize()
        
    # Check for First Last pattern if First Middle Last doesn't match
    elif match := first_last.match(tokenized):
        first, last = match.groups()
        data.at[i, 'first'] = first.capitalize()
        data.at[i, 'last'] = last.capitalize()
        data.at[i, 'middle'] = None  # No middle initial in this case
        
# Count how many are leftover ~ 700: single last names, single letters, weird symbols
leftover = data[data['first'].isna() | data['last'].isna()]

# This is now the data that is identifiable by the patterns we have specified
identified = data[~data['first'].isna() & ~data['last'].isna()]

# How many distinct tokenized names are there ~ 11,887
unique_rows = identified.drop_duplicates(subset='tokenized', keep=False)
distinct = identified['tokenized'].nunique()

# Sort the duplicates by the 'tokenized' column
duplicates = duplicates >> dplyr.arrange(X['tokenized'])

# Sort, remove tokenized column and save to excel
duplicates.to_excel('./merge_duplicates.xlsx', index=False)
