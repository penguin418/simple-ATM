from unittest import TestCase
from unittest.mock import MagicMock

from atm import Atm, AtmExit, AtmAuthorized, AtmDisplayingBalance, AtmProcessingDeposit
from model.domain import CashBox


class Unittest(TestCase):
    def setUp(self):
        # given
        self.atm = Atm(CashBox(cash=1000, limit=5000))
        card = MagicMock()
        card.card_holder = MagicMock()

        account = MagicMock()
        account.balance = 100
        card.card_holder.accounts = [account]
        card.card_holder.accounts[0].balance = 2000

        self.atm.insert_card(card)
        self.atm.enter_pin('1')
        self.atm.select_account(0)

    def test_select_menu(self):
        # when
        self.atm.select_deposit()

        # then
        self.assertEqual(
            AtmProcessingDeposit.get_name(),
            self.atm.get_current_state_name()
        )

    def test_put_valid_amount(self):
        # when
        self.atm.select_deposit()
        self.atm.put_in_cash(100)

        # then
        self.assertEqual(
            AtmDisplayingBalance.get_name(),
            self.atm.get_current_state_name()
        )

    def test_put_invalid_amount(self):
        # when
        self.atm.select_deposit()
        self.atm.put_in_cash(-100)

        # then
        self.assertEqual(
            AtmExit.get_name(),
            self.atm.get_current_state_name()
        )
