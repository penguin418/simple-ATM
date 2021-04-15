from unittest import TestCase
from unittest.mock import MagicMock

from atm import Atm


class IntegrationTest(TestCase):
    atm = None

    @classmethod
    def setUpClass(cls):
        cls.atm = Atm()

    def test0_insert_card(self):
        card = MagicMock()
        IntegrationTest.atm.insert_card(card)

    def test1_enter_pin(self):
        IntegrationTest.atm.enter_pin(12)

    def test2_retrieve_connected_accounts(self):
        IntegrationTest.atm.get_accounts()

    def test3_select_one_of_account(self):
        IntegrationTest.atm.select_account(1)

    def test4_deposit_into_selected_account(self):
        IntegrationTest.atm.deposit(100)

    def test5_withdraw_from_selected_account(self):
        IntegrationTest.atm.withdraw(50)

    def test6_display_balance_from_selected_account(self):
        IntegrationTest.atm.display_balance()

    def test7_leave_system_for_next_person(self):
        IntegrationTest.atm.exit()
