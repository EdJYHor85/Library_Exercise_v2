import pandas as pd

# Load data
library = pd.read_csv("library.csv")
customers = pd.read_csv("library_customers.csv")

# ------------------
# FIND ANOMALIES
# ------------------

def find_missing_values(df):
    print("\nMISSING VALUES")
    print(df[df.isnull().any(axis=1)])


def find_invalid_customer_ids(loans_df, customers_df):
    valid_ids = customers_df["Customer ID"]

    invalid = loans_df[
        ~loans_df["Customer ID"].isin(valid_ids)
    ]

    print("\nINVALID CUSTOMER IDs")
    print(invalid)


def find_duplicate_loans(df):
    duplicates = df[
        df.duplicated(
            subset=[
                "Books",
                "Book checkout",
                "Book Returned",
                "Customer ID"
            ],
            keep=False
        )
    ]

    print("\nDUPLICATE LOANS")
    print(duplicates)


def find_invalid_dates(df):
    invalid_dates = df[
        df["Book checkout"].isin(
            ["10/04/2063", "32/05/2023"]
        )
    ]

    print("\nINVALID DATE VALUES")
    print(invalid_dates)


def find_borrowing_anomalies(df):

    negative = df[df["Days Borrowed"] < 0]
    overdue = df[df["Days Borrowed"] > 14]

    print("\nNEGATIVE BORROWING PERIODS")
    print(negative)

    print("\nBOOKS BORROWED LONGER THAN 14 DAYS")
    print(overdue)


# ------------------
# CLEAN DATA
# ------------------

# Remove completely empty rows
library = library.dropna(how="all")
customers = customers.dropna(how="all")

# Find invalid dates before fixing them
find_invalid_dates(library)

# Remove quotation marks from dates
library["Book checkout"] = (
    library["Book checkout"]
    .astype(str)
    .str.replace('"', '', regex=False)
)

library["Book Returned"] = (
    library["Book Returned"]
    .astype(str)
    .str.replace('"', '', regex=False)
)

# Fix incorrect dates
library["Book checkout"] = library["Book checkout"].replace(
    "10/04/2063",
    "10/04/2023"
)

library["Book checkout"] = library["Book checkout"].replace(
    "32/05/2023",
    "31/05/2023"
)

# Convert to datetime format
library["Book checkout"] = pd.to_datetime(
    library["Book checkout"],
    dayfirst=True
)

library["Book Returned"] = pd.to_datetime(
    library["Book Returned"],
    dayfirst=True
)

# Calculate borrowing duration
library["Days Borrowed"] = (
    library["Book Returned"]
    - library["Book checkout"]
).dt.days

# ------------------
# IDENTIFY ANOMALIES
# ------------------

find_missing_values(library)

find_invalid_customer_ids(
    library,
    customers
)

find_duplicate_loans(library)

find_borrowing_anomalies(library)

# ------------------
# REMOVE BAD DATA
# ------------------

# Remove duplicate loans
library = library.drop_duplicates(
    subset=[
        "Books",
        "Book checkout",
        "Book Returned",
        "Customer ID"
    ]
)

# Remove rows with missing data
library = library.dropna(
    subset=["Books", "Customer ID"]
)

customers = customers.dropna(
    subset=["Customer ID", "Customer Name"]
)

# Remove invalid borrowing periods
library = library[
    (library["Days Borrowed"] >= 0) &
    (library["Days Borrowed"] <= 14)
]

# Remove customer IDs that do not exist
valid_ids = customers["Customer ID"]

library = library[
    library["Customer ID"].isin(valid_ids)
]

# ------------------
# SAVE CLEAN FILES
# ------------------

library.to_csv(
    "library_cleaned.csv",
    index=False
)

customers.to_csv(
    "library_customers_cleaned.csv",
    index=False
)

print("\nDATA CLEANING COMPLETE")
print(f"Clean library records: {len(library)}")
print(f"Clean customer records: {len(customers)}")