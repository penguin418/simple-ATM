from unittest import TestCase
from unittest.mock import MagicMock

from atm import Atm, AtmExit, AtmAuthorized, AtmAccountSelected


class AtmReadyTest(TestCase):
    def setUp(self):
        # given
        self.atm = Atm()
        card = MagicMock()
        card.card_holder = MagicMock()
        card.card_holder.accounts = [MagicMock()]
        self.atm.insert_card(card)
        self.atm.enter_pin('1')

    def test_enter_valid_index(self):
        # when
        self.atm.select_account(0)

        # then
        self.assertEqual(
            AtmAccountSelected.get_name(),
            self.atm.context.current.get_name()
        )


    def test_enter_invalid_index(self):
        # when
        self.atm.select_account(2)

        # then
        self.assertEqual(
            AtmAuthorized.get_name(),
            self.atm.context.current.get_name()
        )
