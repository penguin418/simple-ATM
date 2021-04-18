from unittest import TestCase
from unittest.mock import MagicMock

from atm import Atm, AtmExit, AtmAuthorized, AtmDisplayingBalance, AtmProcessingDeposit


class Unittest(TestCase):
    def setUp(self):
        # given
        self.atm = Atm()
        card = MagicMock()
        card.card_holder = MagicMock()

        account = MagicMock()
        account.balance = 100
        card.card_holder.accounts = [account]

        self.atm.insert_card(card)
        self.atm.enter_pin('1')
        self.atm.select_account(0)

    def test_select_menu(self):
        # when
        self.atm.select_deposit()

        # then
        self.assertEqual(
            AtmProcessingDeposit.get_name(),
            self.atm.context.current.get_name()
        )

    def test_put_valid_amount(self):
        # when
        self.atm.select_deposit()
        self.atm.put_cash(100)

        # then
        self.assertEqual(
            AtmDisplayingBalance.get_name(),
            self.atm.context.current.get_name()
        )

    def test_put_invalid_amount(self):
        # when
        self.atm.select_deposit()
        self.atm.put_cash(-100)

        # then
        self.assertEqual(
            AtmExit.get_name(),
            self.atm.context.current.get_name()
        )
