from unittest import TestCase
from unittest.mock import MagicMock

from atm import Atm, AtmExit, AtmAuthorized


class Unittest(TestCase):
    def setUp(self):
        # given
        self.atm = Atm()
        card = MagicMock()
        card.card_holder = MagicMock()
        card.card_holder.accounts = [MagicMock()]
        self.atm.insert_card(card)

    def test_enter_valid_pin(self):
        # when
        self.atm.enter_pin('1')

        # then
        self.assertEqual(
            AtmAuthorized.get_name(),
            self.atm.context.current.get_name()
        )

    def test_enter_invalid_pin(self):
        # when
        self.atm.enter_pin('2')

        # then
        self.assertEqual(
            AtmExit.get_name(),
            self.atm.context.current.get_name()
        )