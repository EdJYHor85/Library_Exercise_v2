import pandas as pd

# Load data
library = pd.read_csv("library.csv")
customers = pd.read_csv("library_customers.csv")

print (library)

def clean_titles(df):
    out = df.copy()
    out['Books']   = out['Books'].str.strip()
    return out

count_of_trailing_spaces = library['Books'].str.endswith(" ").sum()

print(f"count of whitespace {count_of_trailing_spaces}")

recount_trailing_spaces = clean_titles(library)['Books'].str.endswith(" ").sum()
print(f"recount: {recount_trailing_spaces}")

import pytest
import unittest