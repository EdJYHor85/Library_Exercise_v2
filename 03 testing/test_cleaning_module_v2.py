import pandas as pd
import pytest
import importlib

from pathlib import Path
import sys

#Project root
ROOT = Path(__file__).resolve().parent.parent

#Add the "02 main" folder to Python's search path
sys.path.insert(0, str(ROOT / "02 main"))

from cleaning_module_v2 import (
remove_empty_rows,
convert_dates,
find_duplicate_loans,
remove_invalid_customer_ids,
remove_invalid_borrow_periods
)

# ------------------
# TEST EMPTY CELLS CLEANUP
# ------------------

def test_remove_empty_rows():

    # Arrange
    test_df = pd.DataFrame({
        "Books": ["Dune", None],
        "Customer ID": [1, None]
    })

    # Act
    cleaned_df = remove_empty_rows(test_df)

    # Assert
    assert len(cleaned_df) == 1


# ------------------
# TEST DATA FORMAT CLEANUP
# ------------------

def test_convert_dates():

    # Arrange
    test_df = pd.DataFrame({
        "Book checkout": ["01/04/2023"],
        "Book Returned": ["10/04/2023"]
    })

    # Act
    cleaned_df = convert_dates(test_df)

    # Assert
    assert pd.api.types.is_datetime64_any_dtype(
        cleaned_df["Book checkout"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned_df["Book Returned"]
    )


# ------------------
# TEST DUPLICATE DETECTION
# ------------------

def test_find_duplicate_loans():

    # Arrange
    test_df = pd.DataFrame({
        "Books": [
            "Little Women",
            "Little Women"
        ],
        "Book checkout": [
            "02/04/2023",
            "02/04/2023"
        ],
        "Book Returned": [
            "01/05/2023",
            "01/05/2023"
        ],
        "Customer ID": [1, 1]
    })

    # Act
    duplicates = find_duplicate_loans(test_df)

    # Assert
    assert len(duplicates) == 2


# ------------------
# TEST INVALID CUSTOMER IDS
# ------------------

def test_invalid_customer_ids():

    # Arrange
    loans_df = pd.DataFrame({
        "Customer ID": [1, 10]
    })

    customers_df = pd.DataFrame({
        "Customer ID": [1]
    })

    # Act
    invalid_customers = (
        remove_invalid_customer_ids(
            loans_df,
            customers_df
        )
    )

    # Assert
    assert len(invalid_customers) == 1

    assert (
        invalid_customers["Customer ID"]
        .iloc[0]
        == 1
    )


# ------------------
# TEST BORROWING RULE
# ------------------

def test_remove_invalid_borrow_periods():

    # Arrange
    test_df = pd.DataFrame({
        "Days Borrowed": [
            10,
            20,
            -5
        ]
    })

    # Act
    cleaned_df = (
        remove_invalid_borrow_periods(
            test_df
        )
    )

    # Assert
    assert len(cleaned_df) == 1

    assert (
        cleaned_df.iloc[0]
        ["Days Borrowed"]
        == 10
    )
