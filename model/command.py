import copy
from typing import TYPE_CHECKING

from model.base import SingletonMeta

if TYPE_CHECKING:
    from infra.bank_api import IBankSystem
    from model.domain import CashBox, Account


class IUpdateTransactionCommand(metaclass=SingletonMeta):
    # @abstractmethod
    def execute(self, bank_system, cash_box, account, offset):
        return True


class MockUpdateTransactionCommand(IUpdateTransactionCommand):
    """Mock Update Transaction Command skip the process synchronizing with server

    * Implementation could use another bank api instance
    """

    def execute(self, bank_system, cash_box, account, offset):
        """Update if valid

        Args:
            bank_system (IBankSystem):
            cash_box (CashBox): Atm's cashbox
            account (Account): selected account
            offset (int): Amount to deposit or withdrawal
        """
        old_cash_box_cash = copy.deepcopy(cash_box.cash)
        old_account_balance = copy.deepcopy(account.balance)
        try:
            cash_box.cash += offset
            account.balance += offset
            if offset > 0:  # Deposit
                if cash_box.limit < cash_box.cash + offset:
                    raise ValueError('cannot deposit any more, bin is almost full')
                # Sync with bank system
                # If error occur, raise
            else:  # Withdrawal, offset has negative value
                if account.balance + offset < 0:
                    raise ValueError('atm does not have enough cash')
                if cash_box.cash + offset < 0:
                    raise ValueError('cash box does not have enough cash')
                # Sync with bank system
                # Same as above
        except ValueError as e:
            cash_box.cash = old_cash_box_cash
            account.balance = old_account_balance
            raise ValueError(e)
