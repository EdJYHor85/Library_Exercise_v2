import pandas as pd

# Load the CSV files
library = pd.read_csv("library.csv")
customers = pd.read_csv("library_customers.csv")

# Remove completely empty rows
library = library.dropna(how="all")
customers = customers.dropna(how="all")

# Remove quotation marks from date columns
library["Book checkout"] = library["Book checkout"].astype(str).str.replace('"', '')
library["Book Returned"] = library["Book Returned"].astype(str).str.replace('"', '')

# Fix incorrect dates
library["Book checkout"] = library["Book checkout"].replace(
    "10/04/2063",
    "10/04/2023"
)

library["Book checkout"] = library["Book checkout"].replace(
    "32/05/2023",
    "31/05/2023"
)

# Convert dates into datetime format
library["Book checkout"] = pd.to_datetime(
    library["Book checkout"],
    dayfirst=True
)

library["Book Returned"] = pd.to_datetime(
    library["Book Returned"],
    dayfirst=True
)

# Check for customer IDs that do not exist
valid_ids = customers["Customer ID"].dropna()

print("Invalid Customer IDs")
print(
    library[
        ~library["Customer ID"].isin(valid_ids)
    ]
)

# Remove duplicate records
library = library.drop_duplicates()
customers = customers.drop_duplicates()

# Remove rows with missing book titles or customer IDs
library = library.dropna(subset=["Books", "Customer ID"])

# Save cleaned data
library.to_csv("library_cleaned.csv", index=False)
customers.to_csv("library_customers_cleaned.csv", index=False)