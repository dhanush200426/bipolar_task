from sqlalchemy import case, literal_column
from enum import Enum


class SnackStatus(str, Enum):
    GONE = "gone"
    RUNNING_LOW = "running_low"
    STOCKED = "stocked"


def get_snack_status_case_expression(quantity_column, low_stock_threshold_column):
    """
    Returns a SQLAlchemy CASE expression for deriving snack status.
    
    Logic:
    - quantity = 0 -> gone
    - 1 <= quantity <= low_stock_threshold -> running_low
    - else -> stocked
    """
    return case(
        (quantity_column == 0, literal_column("'gone'")),
        ((quantity_column > 0) & (quantity_column <= low_stock_threshold_column), literal_column("'running_low'")),
        else_=literal_column("'stocked'")
    )


def get_snack_status(quantity: int, low_stock_threshold: int) -> SnackStatus:
    """
    Python function with the same logic as the SQL CASE expression.
    Used for response objects.
    """
    if quantity == 0:
        return SnackStatus.GONE
    elif 1 <= quantity <= low_stock_threshold:
        return SnackStatus.RUNNING_LOW
    else:
        return SnackStatus.STOCKED
