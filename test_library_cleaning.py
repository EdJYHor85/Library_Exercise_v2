import pandas as pd

from library_cleaning import (
    remove_empty_rows,
    fix_dates,
    remove_duplicate_loans,
    remove_invalid_borrow_periods
)

def test_remove_empty_rows():

    # Arrange
    df = pd.DataFrame({
        "Books": ["Dune", None],
        "Customer ID": [1, None]
    })

    # Act
    result = remove_empty_rows(df)

    # Assert
    assert len(result) == 1

def test_fix_dates():

    # Arrange
    df = pd.DataFrame({
        "Book checkout": [
            "10/04/2063",
            "32/05/2023"
        ]
    })

    # Act
    result = fix_dates(df)

    # Assert
    assert result.iloc[0]["Book checkout"] == "10/04/2023"
    assert result.iloc[1]["Book checkout"] == "31/05/2023"

def test_remove_invalid_borrow_periods():

    # Arrange
    df = pd.DataFrame({
        "Book checkout": pd.to_datetime(
            ["01/04/2023"],
            dayfirst=True
        ),
        "Book Returned": pd.to_datetime(
            ["20/04/2023"],
            dayfirst=True
        )
    })

    # Act
    result = remove_invalid_borrow_periods(df)

    # Assert
    assert result.empty

def test_remove_duplicate_loans():

    # Arrange
    df = pd.DataFrame({
        "Books": ["Little Women", "Little Women"],
        "Book checkout": ["02/04/2023", "02/04/2023"],
        "Book Returned": ["01/05/2023", "01/05/2023"],
        "Customer ID": [1, 1]
    })

    # Act
    result = remove_duplicate_loans(df)

    # Assert
    assert len(result) == 1