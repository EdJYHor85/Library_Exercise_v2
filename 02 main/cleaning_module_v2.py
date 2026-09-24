import pandas as pd

MAX_BORROW_DAYS = 14


# ------------------
# FIND ANOMALIES
# ------------------

def find_missing_values(df):
    """Return rows containing missing values."""
    return df[df.isnull().any(axis=1)]


def find_invalid_date_formats(df):
    """Find impossible dates."""

    dates = pd.to_datetime(
        df["Book checkout"].astype(str).str.replace('"', ''),
        dayfirst=True,
        errors="coerce"
    )

    return df[dates.isna()]


def find_future_dates(df):
    """Find checkout dates occurring in the future."""

    dates = pd.to_datetime(
        df["Book checkout"].astype(str).str.replace('"', ''),
        dayfirst=True,
        errors="coerce"
    )

    return df[
        dates > pd.Timestamp.today()
    ]


def find_invalid_customer_ids(loans_df, customers_df):
    """Return records with customer IDs missing from customer data."""

    valid_ids = customers_df["Customer ID"]

    return loans_df[
        ~loans_df["Customer ID"].isin(valid_ids)
    ]


def find_duplicate_loans(df):
    """Return duplicate loan records."""

    return df[
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


def find_borrowing_anomalies(df):
    """Return negative and overdue borrow periods."""

    negative = df[df["Days Borrowed"] < 0]

    overdue = df[
        df["Days Borrowed"] > MAX_BORROW_DAYS
    ]

    return negative, overdue


# ------------------
# CLEANING FUNCTIONS
# ------------------

def remove_empty_rows(df):
    """Remove completely empty rows."""
    return df.dropna(how="all")


def clean_date_columns(df):
    """Remove quotes from date columns."""

    df = df.copy()

    for column in ["Book checkout", "Book Returned"]:
        df[column] = (
            df[column]
            .astype(str)
            .str.replace('"', '', regex=False)
            .str.strip()
        )

    return df


def convert_dates(df):
    """Convert date columns to datetime."""

    df = df.copy()

    df["Book checkout"] = pd.to_datetime(
        df["Book checkout"],
        dayfirst=True,
        errors="coerce"
    )

    df["Book Returned"] = pd.to_datetime(
        df["Book Returned"],
        dayfirst=True,
        errors="coerce"
    )

    return df


def remove_future_dates(df):
    """Remove records with future checkout dates."""

    return df[
        df["Book checkout"] <= pd.Timestamp.today()
    ]


def calculate_days_borrowed(df):
    """Calculate borrowing duration."""

    df = df.copy()

    df["Days Borrowed"] = (
        df["Book Returned"]
        - df["Book checkout"]
    ).dt.days

    return df


def remove_duplicate_loans(df):
    """Remove duplicate loan records."""

    return df.drop_duplicates(
        subset=[
            "Books",
            "Book checkout",
            "Book Returned",
            "Customer ID"
        ]
    )


def remove_missing_data(df):
    """Remove records missing key information."""

    return df.dropna(
        subset=["Books", "Customer ID"]
    )


def remove_invalid_borrow_periods(df):
    """Remove loans with negative or excessive borrowing periods."""

    return df[
        (df["Days Borrowed"] >= 0)
        &
        (df["Days Borrowed"] <= MAX_BORROW_DAYS)
    ]


def remove_invalid_customer_ids(df, customers):
    """Keep only valid customer IDs."""

    valid_ids = customers["Customer ID"]

    return df[
        df["Customer ID"].isin(valid_ids)
    ]


# ------------------
# CLEAN DATASETS
# ------------------

def clean_customers(customers):

    customers = remove_empty_rows(customers)

    customers = customers.dropna(
        subset=[
            "Customer ID",
            "Customer Name"
        ]
    )

    customers = customers.drop_duplicates()

    return customers


def clean_books(library, customers):

    library = remove_empty_rows(library)

    library = clean_date_columns(library)

    library = convert_dates(library)

    library = remove_future_dates(library)

    library = calculate_days_borrowed(library)

    library = remove_duplicate_loans(library)

    library = remove_missing_data(library)

    library = remove_invalid_borrow_periods(library)

    library = remove_invalid_customer_ids(
        library,
        customers
    )

    return library


# ------------------
# RUN SCRIPT
# ------------------

if __name__ == "__main__":

    library = pd.read_csv("01 data\library.csv")
    customers = pd.read_csv("01 data\library_customers.csv")

    print("\nMISSING VALUES")
    print(find_missing_values(library))

    print("\nINVALID DATE FORMATS")
    print(find_invalid_date_formats(library))

    print("\nFUTURE DATES")
    print(find_future_dates(library))

    print("\nDUPLICATE LOANS")
    print(find_duplicate_loans(library))

    print("\nINVALID CUSTOMER IDs")
    print(
        find_invalid_customer_ids(
            library,
            customers
        )
    )

    customers = clean_customers(customers)

    library = clean_books(
        library,
        customers
    )

    print("\nDATA CLEANING COMPLETE")
    print(f"Clean library records: {len(library)}")
    print(f"Clean customer records: {len(customers)}")

    library.to_csv(
        "library_cleaned.csv",
        index=False
    )

    customers.to_csv(
        "library_customers_cleaned.csv",
        index=False
    )