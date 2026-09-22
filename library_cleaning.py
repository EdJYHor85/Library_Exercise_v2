def remove_empty_rows(df):
    return df.dropna(how="all")


def fix_dates(df):
    df = df.copy()

    df["Book checkout"] = df["Book checkout"].replace(
        "10/04/2063",
        "10/04/2023"
    )

    df["Book checkout"] = df["Book checkout"].replace(
        "32/05/2023",
        "31/05/2023"
    )

    return df


def remove_duplicate_loans(df):
    return df.drop_duplicates(
        subset=[
            "Books",
            "Book checkout",
            "Book Returned",
            "Customer ID"
        ]
    )


def remove_invalid_borrow_periods(df):

    df = df.copy()

    df["Days Borrowed"] = (
        df["Book Returned"]
        - df["Book checkout"]
    ).dt.days

    return df[
        (df["Days Borrowed"] >= 0)
        & (df["Days Borrowed"] <= 14)
    ]