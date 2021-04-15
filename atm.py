from typing import TYPE_CHECKING

from model.command import MockValidatePinCommand

if TYPE_CHECKING:
    from model.domain import Card
    from model.command import IValidatePinCommand


class Atm:
    def __init__(self, validate_pin_command=None):
        self.context = AtmContext()
        if validate_pin_command:
            self.context.validate_pin_command = validate_pin_command
        else:
            self.context.validate_pin_command = MockValidatePinCommand()

    def insert_card(self, card):
        """insert card using `AtmWait`

        Args:
            card (Card): current card
        """
        self.context.current.insert_card(card)

    def enter_pin(self, pin):
        """enter pin using `AtmReady`

        Args:
            pin (str): personal identification number
        """
        self.context.current.enter_pin(pin)


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
        self.current = self.states[AtmWait.get_name()]  # type: AtmState
        self.card = None  # type: Card
        self.validate_pin_command = None  # type: IValidatePinCommand

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

    def enter_pin(self, pin):
        """enter pin number in `AtmReady`

        Args:
            pin (str): personal identification number

        Raises:
            ValueError: incorrect pin is entered - when it raised,
              then it does not be changed to `AtmExit`
        """
        raise RuntimeError('restricted behavior')


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

    def enter_pin(self, pin):
        """enter pin number in `AtmReady`

        Args:
            pin (str): personal identification number

        Raises:
            ValueError: incorrect pin is entered - when it raised,
              then it does not be changed to `AtmExit`
        """
        print('enter pin', pin)
        # TODO: verify number from server
        try:
            if self.shared_context.validate_pin_command.execute(
                    self.shared_context.card.card_number,
                    pin
            ):
                self.shared_context.set_state(AtmAuthorized.get_name())
                return True
            else:
                raise ValueError('pin is not matched')
        except ValueError as e:
            self.shared_context.set_state(AtmExit.get_name())
            print(e)


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
