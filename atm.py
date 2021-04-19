import copy
import logging
from typing import TYPE_CHECKING

from infra.bank_api import MockBankSystem1
from model.command import MockUpdateTransactionCommand

if TYPE_CHECKING:
    from model.domain import Card, Account, CashBox
    from infra.bank_api import IBankSystem
    from typing import Callable, NoReturn
    from model.command import IUpdateTransactionCommand


class Atm:
    def __init__(self, cash_box, bank_system=None, update_transaction=None):
        """
        Args:
            cash_box (CashBox): CashBox containing cash, not a physical one
                it must be not null, but set as optional for easier testing

            bank_system (IBankSystem): implementation of Bank System or Mock
            update_transaction (IUpdateTransactionCommand): implementation of update transaction
        """
        self.__context = AtmContext()  # type: AtmContext
        self.__context.cash_box = cash_box
        self.__context.bank_system = bank_system() if bank_system else MockBankSystem1()
        self.__context.update_transaction_command \
            = update_transaction() if update_transaction else MockUpdateTransactionCommand()

    """ATM ACTIONS"""
    def insert_card(self, card):
        """Insert card using `AtmWait`

        Args:
            card (Card): Current card
        """
        self.__context.current.insert_card(card)

    def enter_pin(self, pin):
        """Enter pin using `AtmReady`

        Args:
            pin (str): Personal identification number
        """
        self.__context.current.enter_pin(pin)

    def display_account_list(self):
        """Retrieve copy of accounts connected to card"""
        return self.__context.current.get_accounts()

    def back(self):
        self.__context.current.back()

    def select_account(self, idx):
        """Select account

        Args:
            idx (int): Index of accounts in shared_context, start with 0
        """
        self.__context.current.select_account(idx)

    def select_deposit(self):
        """Select deposit menu"""
        self.__context.current.select_deposit()

    def select_withdraw(self):
        """Select withdraw menu"""
        logger = logging.getLogger()
        self.__context.current.select_withdraw()

    def put_in_cash(self, amount):
        """Put amount into selected account

        Args:
            amount: Amount to be deposited
        """
        self.__context.current.put_cash(amount)

    def enter_withdrawal_amount(self, amount):
        """Enter the amount to withdraw from the selected account

        Args:
            amount (int): Amount to be withdrawn
        """
        self.__context.current.enter_withdrawal_amount(amount)

    def take_out_cash(self, amount):
        """Withdraw the amount from selected account after vault is opened

        Args:
            amount (int): Amount of money to withdraw
        """
        self.__context.current.take_cash(amount)

    def select_balance(self):
        """Select balance"""
        self.__context.current.select_balance()

    def exit(self):
        """Exit system"""
        self.__context.current.exit()

    def take_out_card(self):
        """Take out card in exit state"""
        self.__context.current.remove_card()

    """FOR UI IMPLEMENTATION"""
    def get_selected_account(self):
        """Get selected account object

        * This method designed to support ui
        """
        return copy.deepcopy(self.__context.selected_account)

    def get_inserted_card(self):
        """Get card object

        * This method designed to support ui
        """
        card = copy.deepcopy(self.__context.card)
        return card

    def get_user(self):
        """Get user object

        * This method designed to support ui
        """
        user = copy.deepcopy(self.__context.card.card_holder)
        return user

    def get_current_state_name(self):
        """Get current state

        * This method designed to support ui
        """
        return self.__context.current.get_name()

    def register_on_load(self, on_load_func):
        """Register on load function to be called after changing state

        * This method designed to support ui

        Args:
            on_load_func (function): Function to be called after changing state
        """
        self.__context.register_on_load(on_load_func)


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
        # Initialize first time only
        self.cash_box = None # type: CashBox
        self.bank_system = None  # type: IBankSystem
        self.update_transaction_command = None # type: IUpdateTransactionCommand
        self.on_load_func = None # type: Callable[..., NoReturn]

        # Temporal variables which can be reset on user's leave
        self.current = self.states[AtmWait.get_name()]  # type: AtmState
        self.card = None  # type: Card
        self.accounts = []
        self.selected_account = None  # type: Account
        self.amount_to_withdrawn = 0  # type: int

    def clean_context(self):
        """Clean context

        * It change the current state to AtmWait
        """
        self.current = self.states[AtmWait.get_name()]  # type: AtmState
        self.card = None  # type: Card
        self.accounts = []
        self.selected_account = None  # type: Account
        self.amount_to_withdrawn = 0  # type: int


    def set_state(self, state_name):
        """Set current state by state name

        * All states needs to call this method to change itself to another

        Args:
            state_name (str): Name of next state
        """
        self.current = self.states[state_name]
        self.current.on_load()
        balance = self.selected_account.balance if self.selected_account else 'Not Selected'
        print('[%s card=%s, balance=%s]' % (state_name, self.card, balance))
        if self.on_load_func:
            self.on_load_func()

    def register_on_load(self, on_load_func):
        """Register function which is to be called after change state

        Args:
            on_load_func (function): Function to be called after change state
        """
        self.on_load_func = on_load_func

class AtmState:
    """The default state

    - For all method, it print message `Action is not available in the current state`
    """

    def __init__(self, context):
        """
        Args:
            context (AtmContext): Shared context
        """
        self.shared_context = context

    @classmethod
    def get_name(cls):
        """Return class state_name

        - Class state_name is used for picking next state in `AtmContext`
        """
        return cls.__name__

    def on_load(self):
        pass

    def insert_card(self, card):
        """Insert card in `AtmWait`

        Args:
            card (Card): Current card
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def enter_pin(self, pin):
        """Enter pin number in `AtmReady`

        Args:
            pin (str): Personal identification number

        Raises:
            ValueError: Raised if incorrect pin is entered.

                When raised, then it does not change to `AtmExit`
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def get_accounts(self):
        """Get account list which is connected to card in `AtmAuthorized`

        Returns:
            list[Account]: List of account
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def back(self):
        print('Action is not available in the current state [%s]' % self.get_name())

    def select_account(self, idx):
        """Select account to be used in `AtmAuthorized`

        - When is success, then it changes to `AtmAccountSelected`

        Args:
            idx (int): Index of accounts in shared_context, start with 0

        Raises:
            IndexError: Raised if Idx is not in range of account list - When raised,
                then it changes to `AtmExit`
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def select_deposit(self):
        """Select deposit menu

        * It changes to `AtmProcessingDeposit`
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def select_withdraw(self):
        """Select withdraw menu

        * It changes to `AtmProcessingWithdraw`
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def put_cash(self, amount):
        """Deposit the amount into selected account in `AtmAccountSelected`

        Args:
            amount (int): Amount of money to deposit
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def enter_withdrawal_amount(self, amount):
        """Enter the amount to withdraw from the selected account

        Args:
            amount (int): Amount of money to withdraw
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def take_cash(self, amount):
        """Withdraw the amount from selected account after vault is opened

        Args:
            amount (int): Amount of money to withdraw
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def select_balance(self):
        """Select display balance menu in `AtmAccountSelected`

        * It changes to `AtmDisplayingBalance`
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def exit(self):
        """Select display balance menu in multiple state

        * It changes to `AtmExit`
        """
        print('Action is not available in the current state [%s]' % self.get_name())

    def remove_card(self):
        """Remove card and remove all context variables

        * It changes to ` AtmWait'
        """
        print('Action is not available in the current state [%s]' % self.get_name())


class AtmWait(AtmState):
    """The state waiting for a card (waiting for customers)

    - Have nothing,

    - When a card is inserted th,en it changes to the `AtmReady`
    """

    def insert_card(self, card):
        """Insert card in `AtmWait`

        - If successful, it changes to `AtmReady`.

        Args:
            card (Card): Current card
        """
        print('insert card %s' % card)
        self.shared_context.card = card
        self.shared_context.set_state(AtmReady.get_name())


class AtmReady(AtmState):
    """The state waiting for pin

    - Have card

    - When a pin is entered, then it changes to the `AtmAuthorized`

    - When a back is selected, then it changes to `AtmExit`
    """

    def enter_pin(self, pin):
        """Enter pin number in `AtmReady`

        Args:
            pin (str): Personal identification number

        Raises:
            ValueError: incorrect pin is entered - When raised, it changes to `AtmExit`.
        """
        print('enter pin %s' % pin)
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
            logging.getLogger().warning(e)

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())


class AtmAuthorized(AtmState):
    """The state waiting for selecting account

    - Have card and pin

    - When an account is selected, then it changes to `AtmAccountSelected`

    - When a back-menu is selected, then it changes to `AtmReady`
    """

    def on_load(self):
        self.get_accounts()

    def get_accounts(self):
        """Get account list which is connected to card in `AtmAuthorized`

        Returns:
            list[Account]: List of account

        Raises:
            ReferenceError: Raised if cannot find accounts - When raised, it changes to `AtmExit`.
        """
        try:
            self.shared_context.accounts \
                = self.shared_context.bank_system.get_accounts(self.shared_context.card)
            if len(self.shared_context.accounts) < 1:
                raise RuntimeError('cannot find accounts')
            print('get accounts result=%s' % self.shared_context.accounts)
        except RuntimeError as e:
            print(e)
            self.shared_context.set_state(AtmExit.get_name())
        return copy.deepcopy(self.shared_context.accounts)

    def select_account(self, idx):
        """Select account to be used in `AtmAuthorized`

        - When is success, then It changes to `AtmAccountSelected`

        Args:
            idx (int): Index of accounts in shared_context, start with 0

        Raises:
            IndexError: Raised if idx is not in range of account list - When raised, it does not anything
        """
        try:
            self.shared_context.selected_account \
                = self.shared_context.accounts[idx]
            self.shared_context.set_state(AtmAccountSelected.get_name())
        except IndexError as e:
            print(e)
            print('index starts from 0, candidates=%s' % self.shared_context.accounts)

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())


class AtmAccountSelected(AtmState):
    """The state waiting for selecting transaction

    - Have card, and selected account

    - When a transaction is selected, then It changes to `AtmProcessing~`

    - When a get-menu is selected, then it gives menu

    - When a get-balance is selected, then it gives balance of selected account
    """

    def select_deposit(self):
        """Select deposit menu

        * It changes to `AtmProcessingDeposit`
        """
        self.shared_context.set_state(AtmProcessingDeposit.get_name())

    def select_withdraw(self):
        """Select withdraw menu

        * It changes to `AtmProcessingWithdraw`
        """
        self.shared_context.set_state(AtmPreProcessingWithdrawal.get_name())

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())

    def select_balance(self):
        """Select display balance menu in `AtmAccountSelected`

        * It changes to `AtmDisplayingBalance`
        """
        self.shared_context.set_state(AtmDisplayingBalance.get_name())


    def back(self):
        """ back to `AtmAuthorized`
        """
        self.shared_context.selected_account = None
        self.shared_context.set_state(AtmAuthorized.get_name())

class AtmProcessingDeposit(AtmState):
    """The state processing deposit transaction

    - Have card, and selected account

    - When customer put money, then it changes to `AtmAccountSelected`

    - When customer put less/more money, then it spit out and is changes to
      `AtmExit` while throwing error
    """

    def put_cash(self, amount):
        """Put amount into selected account in `AtmProcessingDeposit`

        Args:
            amount: Amount the customer wants to deposit
        """
        print('put cash %s' % amount)
        try:
            if amount < 0:
                raise ValueError('the amount must be positive')
            # transaction
            self.shared_context.update_transaction_command.execute(
                self.shared_context.bank_system,
                self.shared_context.cash_box,
                self.shared_context.selected_account,
                + amount
            )
            self.shared_context.set_state(AtmDisplayingBalance.get_name())
        except ValueError as e:
            print(e)
            # assume customer withdraw the money in the vault
            self.shared_context.set_state(AtmExit.get_name())

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())

    def back(self):
        """ back to `AtmAccountSelected`

        * Customer canceled deposit
        """
        self.shared_context.set_state(AtmAccountSelected.get_name())

class AtmPreProcessingWithdrawal(AtmState):
    """The state processing withdrawal transaction

    - Have card, and selected account

    - When customer enter amount to withdraw, then it check the balance

    - When account have enough balance, then it changes to
      `AtmProcessingWithdrawal`
    """

    def enter_withdrawal_amount(self, amount):
        """Enter amount customer want to withdraw

        - Check current machine's cash box

        - Check customer's account balance

        Args:
            amount: Amount the customer want to withdraw
        """
        print('enter withdrawal amount %s' % amount)
        try:
            if amount < 0:
                raise ValueError('the amount must be positive')
            if self.shared_context.cash_box.cash < amount:
                raise ValueError('atm does not have enough cash')
            if self.shared_context.selected_account.balance < amount:
                raise ValueError('account does not have enough cash')
            self.shared_context.amount_to_withdrawn = amount
            self.shared_context.set_state(AtmProcessingWithdrawal.get_name())
        except ValueError as e:
            print(str(e))
            self.shared_context.set_state(AtmExit.get_name())

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())

    def back(self):
        """ back to `AtmAccountSelected`

        * Customer canceled withdrawal
        """
        self.shared_context.set_state(AtmAccountSelected.get_name())

class AtmProcessingWithdrawal(AtmState):
    """The state processing withdrawal transaction

    - Have card, selected account and amount_to_withdrawn

    - When customer take money, then it changes to `AtmAccountSelected`

    - When customer try to take more money than s/he got, then it changes to
      `AtmExit` while throwing error
    """

    def take_cash(self, amount):
        """Withdraw the amount from selected account after vault is opened

        * Customer left with out taking cash means customer take 0 cash
        Args:
            amount (int): Amount to withdraw
        """
        print('[take cash %s]' % amount)
        try:
            if amount < 0:
                raise RuntimeError('the amount must be positive')
            if amount > self.shared_context.amount_to_withdrawn:
                raise RuntimeError('the amount must be lower than amount_to_withdrawn')
            # transaction
            self.shared_context.update_transaction_command.execute(
                self.shared_context.bank_system,
                self.shared_context.cash_box,
                self.shared_context.selected_account,
                - amount
            )
            self.shared_context.set_state(AtmDisplayingBalance.get_name())
        except ValueError as e:
            print(e)
            self.shared_context.set_state(AtmDisplayingBalance.get_name())

    def exit(self):
        self.shared_context.selected_account.balance += self.shared_context.amount_to_withdrawn
        self.shared_context.set_state(AtmExit.get_name())

    def back(self):
        """ back to `AtmPreProcessingWithdrawal`

        * May be Customer wants to change amount to withdrawn
        """
        self.shared_context.amount_to_withdrawn = 0
        self.shared_context.set_state(AtmPreProcessingWithdrawal.get_name())

class AtmDisplayingBalance(AtmState):
    """The state displaying balance

    - Have card, and selected account

    - When each transaction finished, then those states change to this
      state

    - Cannot go back to former state
    """

    def on_load(self):
        account = self.shared_context.selected_account
        print('[on load\naccount_number: %s,\naccount_holder: %s,\naccount_balance:%s]' % (
            account.account_number, account.name, account.balance))

    def back(self):
        """Go back to accounts"""
        self.shared_context.set_state(AtmAuthorized.get_name())

    def exit(self):
        self.shared_context.set_state(AtmExit.get_name())


class AtmExit(AtmState):
    """The state pull out card

    - Have card to give back

    - When customer take card, then it changes to `AtmWait`
    """

    def back(self):
        """print message"""
        print('take card, then atm changes to initial state')

    def remove_card(self):
        self.shared_context.clean_context()
