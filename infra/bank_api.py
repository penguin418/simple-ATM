from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

if TYPE_CHECKING:
    from model.domain import Card, User

class IBankSystem(metaclass=ABCMeta):
    """bank system interface for future"""

    @abstractmethod
    def validate_pin(self, card_number, pin):
        """ verify pin number using server
        Args:
            card_number (str): card number
            pin (str): personal identification number likes '1111' or '1111-k' or else.
        """
        pass

    @abstractmethod
    def get_accounts(self, card):
        """retrieve all accounts connected to card"""
        pass


def mock_server_api(x, y):
    return y == '1'


class MockBankSystem1(IBankSystem):
    """mock banking system"""

    def __init__(self):
        # guess server return True
        self.__get_account_pin_api = MagicMock(side_effect=mock_server_api)

    def validate_pin(self, card_number, pin):
        """ verify pin number using server
        Args:
            card_number (str): card number
            pin (str): personal identification number likes '1111' or '1111-k' or else.
        """
        # using bank system
        return self.__get_account_pin_api(card_number, pin)

    def get_accounts(self, card):
        """retrieve all accounts connected to card

        - since this is mock class, it skip retrieving accounts

        - instead it return account from card

        - i assumed that it would retrieve accounts using join query

        Args:
            card (Card): card
        """
        return card.card_holder.accounts
