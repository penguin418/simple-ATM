from typing import TYPE_CHECKING

from infra.bank_api import MockBankSystem1, IBankSystem

if TYPE_CHECKING:
    from model.domain import Card, Account


class Atm:
    def __init__(self, bank_system=None):
        """
        Args:
            bank_system:
        """
        self.context = AtmContext()  # type: AtmContext
        self.context.bank_system = bank_system() if bank_system else MockBankSystem1()

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

    def get_accounts(self):
        """retrieve accounts connected to card"""
        self.context.current.get_accounts()

    def back_to_accounts(self):
        self.context.current.back_to_accounts()

    def select_account(self, idx):
        """select account

        Args:
            idx (int): index of accounts in shared_context, start with 0
        """
        self.context.current.select_account(idx)

    def select_deposit(self):
        """select deposit
        """
        self.context.current.select_deposit()

    def select_withdraw(self):
        """select withdraw
        """
        self.context.current.select_withdraw()

    def put_cash(self, amount):
        """put amount into selected account

        Args:
            amount:
        """
        self.context.current.put_cash(amount)

    def enter_withdrawal_amount(self, amount):
        """enter the amount to withdraw from the selected account

        Args:
            amount (int): amount of money to withdraw
        """
        self.context.current.enter_withdrawal_amount(amount)

    def take_cash(self, amount):
        """withdraw the amount from selected account after vault is opened

        Args:
            amount (int): amount of money to withdraw
        """
        self.context.current.take_cash(amount)

    def select_balance(self):
        """select balance"""
        self.context.current.select_balance()

    def exit(self):
        """exit system"""
        self.context.current.exit()

    def take_card(self):
        """take card in exit state"""
        self.context.current.remove_card()

class AtmContext:
    def __init__(self):
        self.states = {
            AtmWait.get_name(): AtmWait(self),
            AtmReady.get_name(): AtmReady(self),
            AtmAuthorized.get_name(): AtmAuthorized(self),
            AtmAccountSelected.get_name(): AtmAccountSelected(self),
            AtmProcessingDeposit.get_name(): AtmProcessingDeposit(self),
            AtmPreProcessingWithdrawal.get_name(): AtmPreProcessingWithdrawal(self),
            AtmProcessingWithdrawal.get_name(): AtmProcessingWithdrawal(self),
            AtmDisplayingBalance.get_name(): AtmDisplayingBalance(self),
            AtmExit.get_name(): AtmExit(self),
        }
        self.current = self.states[AtmWait.get_name()]  # type: AtmState
        self.card = None  # type: Card
        self.accounts = []
        self.selected_account = None  # type: Account
        self.bank_system = None  # type: IBankSystem
        self.amount_to_withdraw = 0  # type: int

    def clean_context(self):
        self.current = self.states[AtmWait.get_name()]  # type: AtmState
        self.card = None  # type: Card
        self.accounts = []
        self.selected_account = None  # type: Account
        self.bank_system = None  # type: IBankSystem
        self.amount_to_withdraw = 0  # type: int

    def set_state(self, state_name):
        """set current state by state name

        Args:
            state_name (str): name of next state
        """
        print('next state is', state_name)
        self.current = self.states[state_name]
        self.current.on_load()


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

    def on_load(self):
        pass

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
            ValueError: incorrect pin is entered - when it raised, then it does
                not be changed to `AtmExit`
        """
        raise RuntimeError('restricted behavior')

    def get_accounts(self):
        raise RuntimeError('restricted behavior')

    def back_to_accounts(self):
        raise RuntimeError('restricted behavior')

    def select_account(self, idx):
        """select account to be used in `AtmAuthorized`

        - when is success, then it's changed to `AtmAccountSelected`

        Args:
            idx (int): index of accounts in shared_context, start with 0

        Raises:
            IndexError: idx is not in range of account list - when it's raised,
                then it's changed to `AtmExit`
        """
        raise RuntimeError('restricted behavior')

    def select_deposit(self):
        """select deposit menu

        * it's changed to `AtmProcessingDeposit`
        """
        raise RuntimeError('restricted behavior')

    def select_withdraw(self):
        """select withdraw menu

        * it's changed to `AtmProcessingWithdraw`
        """
        raise RuntimeError('restricted behavior')

    def put_cash(self, amount):
        """deposit the amount into selected account in `AtmAccountSelected`

        Args:
            amount (int): amount of money to deposit
        """
        raise RuntimeError('restricted behavior')

    def enter_withdrawal_amount(self, amount):
        """enter the amount to withdraw from the selected account

        Args:
            amount (int): amount of money to withdraw
        """
        raise RuntimeError('restricted behavior')

    def take_cash(self, amount):
        """withdraw the amount from selected account after vault is opened

        Args:
            amount (int): amount of money to withdraw
        """
        raise RuntimeError('restricted behavior')

    def select_balance(self):
        """select display balance menu in `AtmAccountSelected`

        * it's changed to `AtmDisplayingBalance`
        """
        raise RuntimeError('restricted behavior')

    def exit(self):
        """select display balance menu in multiple state

        * it's changed to `AtmExit`
        """
        raise RuntimeError('restricted behavior')

    def remove_card(self):
        """remove card and remove all context variables

        * it's changed to `AtmWait'
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
            ValueError: incorrect pin is entered - when it raised, then it does
                not be changed to `AtmExit`
        """
        print('enter pin', pin)
        # TODO: verify number from server
        try:
            if self.shared_context.bank_system.validate_pin(
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

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())

class AtmAuthorized(AtmState):
    """The state waiting for selecting account

    - having card and pin

    - when an account is selected, then it's changed to `AtmAccountSelected`

    - when a back-menu is selected, then it's changed to `AtmReady`
    """

    def on_load(self):
        self.get_accounts()

    def get_accounts(self):
        """get account list which is connected to card in `AtmAuthorized`

        Returns:
            list[Account]: list of account

        Raises:
            ReferenceError: cannot find accounts - when it's raised, then it's
                changed to `AtmExit`
        """
        try:
            self.shared_context.accounts \
                = self.shared_context.bank_system.get_accounts(self.shared_context.card)
            if len(self.shared_context.accounts) < 1:
                raise RuntimeError('cannot find accounts')
            print('get accounts result=', self.shared_context.accounts)
        except RuntimeError as e:
            print(e)
            self.shared_context.set_state(AtmExit.get_name())
        return self.shared_context.accounts

    def select_account(self, idx):
        """select account to be used in `AtmAuthorized`

        - when is success, then it's changed to `AtmAccountSelected`

        Args:
            idx (int): index of accounts in shared_context, start with 0

        Raises:
            IndexError: idx is not in range of account list - when it's raised,
                then it's changed to `AtmExit`
        """
        try:
            self.shared_context.selected_account \
                = self.shared_context.accounts[idx]
            self.shared_context.set_state(AtmAccountSelected.get_name())
        except IndexError as e:
            print(e)
            print('please choose again, index starts from 0, candidates=', self.shared_context.accounts)

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())

class AtmAccountSelected(AtmState):
    """The state waiting for selecting transaction

    - having card, pin, and selected account

    - when a transaction is selected, then it's changed to `AtmProcessing~`

    - when a get-menu is selected, then it gives menu

    - when a get-balance is selected, then it gives balance of selected account
    """

    def select_deposit(self):
        """select deposit menu

        * it's changed to `AtmProcessingDeposit`
        """
        self.shared_context.set_state(AtmProcessingDeposit.get_name())

    def select_withdraw(self):
        """select withdraw menu

        * it's changed to `AtmProcessingWithdraw`
        """
        self.shared_context.set_state(AtmPreProcessingWithdrawal.get_name())

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())

    def select_balance(self):
        """select display balance menu in `AtmAccountSelected`

        * it's changed to `AtmDisplayingBalance`
        """
        self.shared_context.set_state(AtmDisplayingBalance.get_name())

class AtmProcessingDeposit(AtmState):
    """The state processing deposit transaction

    - having card, pin, and selected account

    - when customer put money, then it's changed to `AtmAccountSelected`

    - when customer put less/more money, then it spit out and is changed to
      `AtmExit` while throwing error
    """

    def put_cash(self, amount):
        """put amount into selected account in `AtmProcessingDeposit`

        Args:
            amount: the amount the customer wants to deposit
        """
        print('put cash', amount)
        try:
            if amount < 0:
                raise ValueError('the amount must be positive')
            self.shared_context.selected_account.balance += amount
            self.shared_context.set_state(AtmDisplayingBalance.get_name())
        except ValueError as e:
            print(e)
            self.shared_context.set_state(AtmExit.get_name())

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())

class AtmPreProcessingWithdrawal(AtmState):
    """The state processing withdrawal transaction

    - having card, pin, and selected account

    - when customer enter amount to withdraw, then it check the balance

    - if account have enough balance, then it's changed to `AtmProcessingWithdrawal`
    """
    def enter_withdrawal_amount(self, amount):
        """enter amount customer want to withdraw

        - check current machine's checkbox

        - check customer's account balance
        """
        print('enter withdrawal amount', amount)
        try:
            if amount < 0:
                raise ValueError('the amount must be positive')
            self.shared_context.amount_to_withdraw = amount
            self.shared_context.set_state(AtmProcessingWithdrawal.get_name())
        except ValueError as e:
            print(e)
            self.shared_context.set_state(AtmExit.get_name())

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())

class AtmProcessingWithdrawal(AtmState):
    """The state processing withdrawal transaction

    - having card, pin, and selected account

    - when customer take money, then it's changed to `AtmAccountSelected`

    - when customer try to take more money than s/he got, then it's changed to
      `AtmExit` while throwing error
    """

    def take_cash(self, amount):
        """withdraw the amount from selected account after vault is opened

        Args:
            amount (int): amount of money to withdraw
        """
        print('take cash', amount)
        try:
            if amount < 0:
                raise ValueError('the amount must be positive')
            if amount < self.shared_context.amount_to_withdraw:
                self.shared_context.selected_account.balance += (self.shared_context.amount_to_withdraw - amount)
            self.shared_context.set_state(AtmDisplayingBalance.get_name())
        except ValueError as e:
            print(e)
            self.shared_context.set_state(AtmExit.get_name())

    def exit(self):
        self.shared_context.selected_account.balance += self.shared_context.amount_to_withdraw
        self.shared_context.set_state(AtmExit.get_name())

class AtmDisplayingBalance(AtmState):
    """The state displaying balance

    - having card, pin, and selected account

    - when each transaction finished, then those states are changed to this state

    - cannot go back to former state
    """

    def on_load(self):
        print(self.shared_context.selected_account)

    def back_to_accounts(self):
        self.shared_context.set_state(AtmAuthorized.get_name())

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())

class AtmExit(AtmState):
    """The state pull out card

    - having card to give back

    - when customer take card, then it's changed to `AtmWait`
    """
    def remove_card(self):
        self.shared_context.clean_context()
