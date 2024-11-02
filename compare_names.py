"""
Author: Nathan Malamud
Date: Thursday, Oct 19th, 2024

Goal: Compare two names, even if they are different variations of the same name,
and return True if they are the same name and False if they are different.

Original Author: Audra
Source: Converted from R to Python using ChatGPT-4 
        (https://chatgpt.com/share/6713fea2-4c18-8012-a14f-647296cd18aa)
"""

import pandas as pd
import re
from Levenshtein import distance as lev_distance

# Tokenize names: clean, split, and remove stop words
def tokenize(name):
    clean_name = name.lower().strip()  # Lowercase and strip whitespace
    tokens = re.split(r'[\s.]+', clean_name)  # Split by spaces or dots
    # Remove stop words and empty tokens
    return [t for t in tokens if t not in ['and', 'or', 'is', '']]

# Standardize tokens: sort and remove duplicates
def standardize(tokens):
    return sorted(set(tokens))  # Sort and remove duplicates

# Compare two names using Levenshtein distance
def compare_names(name1, name2, threshold=0.8):
    tokens1 = tokenize(name1)
    tokens2 = tokenize(name2)
    
    # Standardize tokens
    std_tokens1 = standardize(tokens1)
    std_tokens2 = standardize(tokens2)
    
    # Calculate total Levenshtein distance
    max_len = max(len(std_tokens1), len(std_tokens2))
    total_distance = lev_distance(" ".join(std_tokens1), " ".join(std_tokens2))
    
    # Calculate similarity score
    similarity = 1 - (total_distance / max_len)
    
    return similarity >= threshold  # Return True if similar

def main():
    """
    Code demo driver for comparing names.
    Loads names from an Excel file, standardizes them, and checks for matches.
    """
    # Load the Excel file
    file_path = "Names/Names to Standardise.xlsx"
    df = pd.read_excel(file_path, skiprows=1)

    # Drop irrelevant columns
    df = df.drop(df.columns[[5, 6, 7]], axis=1)

    # Create 'Combined Name' by concatenating first, middle, and last names
    df['Combined Name'] = df[['First.Name', 'Middle.Initial', 'Last.Name']].fillna('').agg(' '.join, axis=1).str.strip()

    # Compare each name with its standardized version
    df['Match'] = df.apply(lambda row: compare_names(row['Combined Name'], row['Standardized Name']), axis=1)

    # Display the DataFrame with results
    print(df[['Combined Name', 'Standardized Name', 'Match']])

if __name__ == '__main__':
    main()
