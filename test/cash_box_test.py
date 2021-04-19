from unittest import TestCase
from unittest.mock import MagicMock

from atm import Atm, AtmExit, AtmAuthorized
from model.domain import CashBox


class Unittest(TestCase):
    def setUp(self):
        # given
        self.atm = Atm(CashBox(cash=1000, limit=2000))
        card = MagicMock()
        card.card_holder = MagicMock()

        account = MagicMock()
        account.balance = 100
        card.card_holder.accounts = [account]
        card.card_holder.accounts[0].balance = 3000

        self.atm.insert_card(card)
        self.atm.enter_pin('1')
        self.atm.select_account(0)

    def test_cash_box_overflow(self):
        # when
        self.atm.select_deposit()
        self.atm.put_in_cash(1500)

        # then
        self.assertEqual(
            AtmExit.get_name(),
            self.atm.get_current_state_name()
        )

    def test_enter_overflow2(self):
        # when
        self.atm.select_withdraw()
        self.atm.enter_withdrawal_amount(1500)
        self.atm.take_out_cash(1500)

        # then
        self.assertEqual(
            AtmExit.get_name(),
            self.atm.get_current_state_name()
        )