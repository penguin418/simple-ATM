from enum import Enum


class ErrorCode(Enum):
    # program related error 1xxx
    AMOUNT_MUST_BE_POSITIVE = 1001

    # card related error 2xxx
    PIN_IS_NOT_MATCHED = 2001

    # account related error 3xxx
    CANNOT_FIND_ACCOUNT = 3001
    WRONG_ACCOUNT_SELECTED = 3001
    ACCOUNT_DOES_NOT_HAVE_ENOUGH_CASH = 3002
    AMOUNT_MUST_BE_LOWER_THAN_AMOUNT_TO_BE_WITHDRAWN = 3003

    # cash box related error 4xxx
    CASH_BOX_DOES_NOT_HAVE_ENOUGH_CASH = 4001
    CASH_BOX_DOES_NOT_HAVE_ENOUGH_SPACE = 4002
