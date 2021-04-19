from unittest import TestCase
from unittest.mock import MagicMock

from atm import Atm, AtmReady, AtmExit, AtmProcessingWithdrawal, AtmProcessingDeposit, AtmAccountSelected, \
    AtmAuthorized, AtmDisplayingBalance, AtmPreProcessingWithdrawal, AtmWait
from model.domain import CashBox

initial_balance = 500
amount_deposit = 100
amount_withdrawal = 50


class IntegrationTest(TestCase):
    atm = None

    @classmethod
    def setUpClass(cls):
        cls.atm = Atm(CashBox(cash=1000, limit=5000))

    def test0_insert_card(self):
        # given
        card = MagicMock()
        card.card_holder = MagicMock()
        card.card_holder.accounts = [MagicMock()]
        card.card_holder.accounts[0].balance = initial_balance

        # when
        IntegrationTest.atm.insert_card(card)

        # then
        self.assertEqual(
            AtmReady.get_name(),
            self.atm.get_current_state_name()
        )

    def test1_enter_pin(self):
        # when
        IntegrationTest.atm.enter_pin('1')

        # then
        self.assertEqual(
            AtmAuthorized.get_name(),
            self.atm.get_current_state_name()
        )

    def test2_retrieve_connected_accounts(self):
        # when
        IntegrationTest.atm.display_account_list()

        # then
        self.assertEqual(
            AtmAuthorized.get_name(),
            self.atm.get_current_state_name()
        )

    def test3_select_one_of_account(self):
        # when
        IntegrationTest.atm.select_account(0)

        # then
        self.assertEqual(
            AtmAccountSelected.get_name(),
            self.atm.get_current_state_name()
        )

    def test4_1_select_deposit(self):
        # when
        IntegrationTest.atm.select_deposit()

        # then
        self.assertEqual(
            AtmProcessingDeposit.get_name(),
            self.atm.get_current_state_name()
        )

    def test4_2_deposit_into_selected_account(self):
        # when
        IntegrationTest.atm.put_in_cash(amount_deposit)

        # then
        self.assertEqual(
            AtmDisplayingBalance.get_name(),
            self.atm.get_current_state_name()
        )

        self.assertEqual(
            initial_balance + amount_deposit,
            self.atm.get_selected_account().balance
        )

    def test4_3_go_back_to_atm_account_selected(self):
        # when
        IntegrationTest.atm.back()

        # then
        self.assertEqual(
            AtmAuthorized.get_name(),
            self.atm.get_current_state_name()
        )

    def test5_0_select_withdraw(self):
        # first, move to atm selected state
        IntegrationTest.atm.select_account(0)

        # when
        IntegrationTest.atm.select_withdraw()

        # then
        self.assertEqual(
            AtmPreProcessingWithdrawal.get_name(),
            self.atm.get_current_state_name()
        )

    def test5_1_enter_withdraw_ammount(self):
        # when
        IntegrationTest.atm.enter_withdrawal_amount(amount_withdrawal)

        # then
        self.assertEqual(
            AtmProcessingWithdrawal.get_name(),
            self.atm.get_current_state_name()
        )

    def test5_2_withdraw_from_selected_account(self):
        # when
        IntegrationTest.atm.take_out_cash(amount_withdrawal)

        # then
        self.assertEqual(
            AtmDisplayingBalance.get_name(),
            self.atm.get_current_state_name()
        )

        self.assertEqual(
            initial_balance + amount_deposit - amount_withdrawal,
            self.atm.get_selected_account().balance
        )

    def test5_3_go_back_to_atm_account_selected(self):
        # when
        IntegrationTest.atm.back()

        # then
        self.assertEqual(
            AtmAuthorized.get_name(),
            self.atm.get_current_state_name()
        )

    def test6_display_balance_from_selected_account(self):
        # first, move to atm selected state
        IntegrationTest.atm.select_account(0)

        # when
        IntegrationTest.atm.select_balance()

        # then
        self.assertEqual(
            AtmDisplayingBalance.get_name(),
            self.atm.get_current_state_name()
        )

    def test7_leave_system(self):
        # when
        IntegrationTest.atm.exit()

        # then
        self.assertEqual(
            AtmExit.get_name(),
            self.atm.get_current_state_name()
        )

    def test8_remove_card(self):
        # when
        IntegrationTest.atm.take_out_card()

        # then
        self.assertEqual(
            AtmWait.get_name(),
            self.atm.get_current_state_name()
        )
