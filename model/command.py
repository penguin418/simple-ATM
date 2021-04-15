from abc import ABCMeta, abstractmethod
from unittest.mock import MagicMock


class IValidatePinCommand(metaclass=ABCMeta):
    """command interface verifying pin using server"""

    @abstractmethod
    def execute(self, card_number, pin):
        """
        Args:
            card_number (str): card number
            pin (str): personal identification number likes '1111' or '1111-k' or else.
        """
        pass


def mock_server_api(x, y):
    return y == '1'


class MockValidatePinCommand(IValidatePinCommand):
    """mock bank system for verifying pin"""

    def __init__(self):
        mock_bank = MagicMock()
        mock_bank.verify_pin_api = MagicMock(side_effect=mock_server_api)
        self.bank_system = mock_bank

    def execute(self, card_number, pin):
        """ verify pin number using banking system of `mock bank`
        Args:
            card_number (str): card number
            pin (str): personal identification number likes '1111' or '1111-k' or else.
        """
        # using bank system
        print(card_number, pin)
        result = self.bank_system.verify_pin_api(card_number, pin)
        return result
# etc ...
