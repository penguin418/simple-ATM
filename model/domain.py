from dataclasses import dataclass


@dataclass
class User:
    """User of card and account"""
    name: str  # type: str
    cards: list  # type: list[Card]
    accounts: list  # type: list[Account]


@dataclass
class Card:
    """Card class"""
    name: str  # type: str
    card_number: str  # type: str
    card_holder: User  # type: User


@dataclass
class Account:
    """Account

    - Originally stored in bank service, but currently let's assumed it stored in cache
    """
    name: str  # type: str
    account_number: str  # type: str
    balance: int  # type: int


@dataclass
class CashBox:
    """Cash box

    Args:
        cash (int): Cash in the box
        limit (int): limit of cash box bin catalog
    """
    cash: int
    limit: int
