from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.domain import Card


class Atm:
    def __init__(self):
        self.context = AtmContext()

    def insert_card(self, card):
        """insert card using `AtmWait`

        Args:
            card (Card): current card
        """
        self.context.current.insert_card(card)


class AtmContext:
    def __init__(self):
        self.states = {
            AtmWait.get_name(): AtmWait(self),
            AtmReady.get_name(): AtmReady(self),
            AtmAuthorized.get_name(): AtmAuthorized(self),
            AtmAccountSelected.get_name(): AtmAccountSelected(self),
            AtmProcessingDeposit.get_name(): AtmProcessingDeposit(self),
            AtmProcessingWithdrawal.get_name(): AtmProcessingWithdrawal(self),
            AtmExit.get_name(): AtmExit(self),
        }
        self.current = self.states[AtmWait.get_name()]
        self.card = None

    def set_state(self, state_name):
        """set current state by state name

        Args:
            state_name (str): name of next state
        """
        self.current = self.states[state_name]


class AtmState:
    """The default state

    - for all method, it return `restricted behaviour`
    """

    def __init__(self, context):
        """
        Args:
            context (AtmContext): shared context
        """
        self.shared_context = context

    @classmethod
    def get_name(cls):
        """return class state_name

        - class state_name is used for picking next state in `AtmContext`
        """
        return cls.__name__

    def insert_card(self, card):
        """insert card in `AtmWait`

        Args:
            card (Card): current card
        """
        raise RuntimeError('restricted behaviour')


class AtmWait(AtmState):
    """The state waiting for a card (waiting for customers)

    - having nothing,

    - when a card is inserted th,en it's changed to the `AtmReady`
    """

    def insert_card(self, card):
        """insert card in `AtmWait`

        - when success, then it's changed to `AtmReady`
        Args:
            card (Card): current card
        """
        print('insert card', card)
        self.shared_context.card = card
        self.shared_context.set_state(AtmReady.get_name())


class AtmReady(AtmState):
    """The state waiting for pin

    - having card

    - when a pin is entered, then it's changed to the `AtmAuthorized`

    - when a back is selected, then it's changed to `AtmExit`
    """
    pass


class AtmAuthorized(AtmState):
    """The state waiting for selecting account

    - having card and pin

    - when an account is selected, then it's changed to `AtmAccountSelected`

    - when a back-menu is selected, then it's changed to `AtmReady`
    """

    pass


class AtmAccountSelected(AtmState):
    """The state waiting for selecting transaction

    - having card, pin, and selected account

    - when a transaction is selected, then it's changed to `AtmProcessing~`

    - when a get-menu is selected, then it gives menu

    - when a get-balance is selected, then it gives balance of selected account
    """

    pass


class AtmProcessingDeposit(AtmState):
    """The state processing deposit transaction

    - having card, pin, and selected account

    - when customer put money, then it's changed to `AtmAccountSelected`

    - when customer put less/more money, then it spit out and is changed to
      `AtmExit` while throwing error
    """
    pass


class AtmProcessingWithdrawal(AtmState):
    """The state processing withdrawal transaction

    - having card, pin, and selected account

    - when customer take money, then it's changed to `AtmAccountSelected`

    - when customer try to take more money than s/he got, then it's changed to
      `AtmExit` while throwing error
    """
    pass


class AtmExit(AtmState):
    """The state pull out card

    - having card to give back

    - when customer take card, then it's changed to `AtmWait`
    """
