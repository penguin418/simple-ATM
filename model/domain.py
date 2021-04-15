from dataclasses import dataclass


@dataclass
class User:
    """user of card and account"""
    name: str  # type: str
    cards: list  # type: list[Card]
    accounts: list  # type: list[Account]


@dataclass
class Card:
    """card class"""
    name: str  # type: str
    card_number: str  # type: str
    card_holder: User  # type: User


@dataclass
class Account:
    """account

    - originally stored in bank service, but currently let's assumed it stored in cache
    """
    name: str  # type: str
    account_number: str  # type: str
    balance: int  # type: int
