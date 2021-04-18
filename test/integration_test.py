from unittest import TestCase
from unittest.mock import MagicMock

from atm import Atm, AtmReady, AtmExit, AtmProcessingWithdrawal, AtmProcessingDeposit, AtmAccountSelected, \
    AtmAuthorized, AtmDisplayingBalance, AtmPreProcessingWithdrawal


class IntegrationTest(TestCase):
    atm = None

    @classmethod
    def setUpClass(cls):
        cls.atm = Atm()

    def test0_insert_card(self):
        # given
        card = MagicMock()
        card.card_holder = MagicMock()
        card.card_holder.accounts = [MagicMock()]

        # when
        IntegrationTest.atm.insert_card(card)

        # then
        self.assertEqual(
            AtmReady.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test1_enter_pin(self):
        # when
        IntegrationTest.atm.enter_pin('1')

        # then
        self.assertEqual(
            AtmAuthorized.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test2_retrieve_connected_accounts(self):
        # when
        IntegrationTest.atm.get_accounts()

        # then
        self.assertEqual(
            AtmAuthorized.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test3_select_one_of_account(self):
        # when
        IntegrationTest.atm.select_account(0)

        # then
        self.assertEqual(
            AtmAccountSelected.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test4_1_select_deposit(self):
        # when
        IntegrationTest.atm.select_deposit()

        # then
        self.assertEqual(
            AtmProcessingDeposit.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test4_2_deposit_into_selected_account(self):
        # when
        IntegrationTest.atm.put_cash(100)

        # then
        self.assertEqual(
            AtmDisplayingBalance.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test4_3_go_back_to_atm_account_selected(self):
        # when
        IntegrationTest.atm.back_to_accounts()

        # then
        self.assertEqual(
            AtmAuthorized.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test5_0_select_withdraw(self):
        # first, move to atm selected state
        IntegrationTest.atm.select_account(0)

        # when
        IntegrationTest.atm.select_withdraw()

        # then
        self.assertEqual(
            AtmPreProcessingWithdrawal.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test5_1_enter_withdraw_ammount(self):
        # when
        IntegrationTest.atm.enter_withdrawal_amount(50)

        # then
        self.assertEqual(
            AtmProcessingWithdrawal.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test5_2_withdraw_from_selected_account(self):
        # when
        IntegrationTest.atm.take_cash(50)

        # then
        self.assertEqual(
            AtmDisplayingBalance.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test5_3_go_back_to_atm_account_selected(self):
        # when
        IntegrationTest.atm.back_to_accounts()

        # then
        self.assertEqual(
            AtmAuthorized.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test6_display_balance_from_selected_account(self):
        # first, move to atm selected state
        IntegrationTest.atm.select_account(0)

        # when
        IntegrationTest.atm.display_balance()

        # then
        self.assertEqual(
            AtmDisplayingBalance.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test7_leave_system_for_next_person(self):
        # when
        IntegrationTest.atm.exit()

        # then
        self.assertEqual(
            AtmExit.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )
