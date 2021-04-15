from unittest import TestCase
from unittest.mock import MagicMock

from atm import Atm, AtmReady, AtmExit, AtmProcessingWithdrawal, AtmProcessingDeposit, AtmAccountSelected, AtmAuthorized


class IntegrationTest(TestCase):
    atm = None

    @classmethod
    def setUpClass(cls):
        cls.atm = Atm()

    def test0_insert_card(self):
        # given
        card = MagicMock()

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
        IntegrationTest.atm.select_account(1)

        # then
        self.assertEqual(
            AtmAccountSelected.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test4_deposit_into_selected_account(self):
        # when
        IntegrationTest.atm.deposit(100)

        # then
        self.assertEqual(
            AtmProcessingDeposit.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test5_withdraw_from_selected_account(self):
        # when
        IntegrationTest.atm.withdraw(50)

        # then
        self.assertEqual(
            AtmProcessingWithdrawal.get_name(),
            IntegrationTest.atm.context.current.get_name()
        )

    def test6_display_balance_from_selected_account(self):
        # when
        IntegrationTest.atm.display_balance()

        # then
        self.assertEqual(
            AtmReady.get_name(),
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
