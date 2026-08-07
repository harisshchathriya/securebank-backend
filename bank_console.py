from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import DefaultDict, Dict, List, Optional


# ==================== 1. CUSTOM EXCEPTIONS ====================
class AccountNotFoundError(Exception):
    """Raised when account ID doesn't exist."""


class InsufficientFundsError(Exception):
    """Raised when withdrawal exceeds balance."""


class InvalidAmountError(Exception):
    """Raised when amount is <= 0."""


# ==================== 2. DATA CLASSES ====================
@dataclass
class Account:
    account_id: int
    name: str
    balance: float = 0.0


@dataclass
class Transaction:
    transaction_type: str
    amount: float
    source_account: Optional[int]
    target_account: Optional[int]
    timestamp: datetime


# ==================== 3. IN-MEMORY LEDGER (HASHMAP/DICT) ====================
accounts: Dict[int, Account] = {}
transaction_history: Dict[int, List[Transaction]] = defaultdict(list)
customer_index: DefaultDict[str, List[int]] = defaultdict(list)


def _get_account(account_id: int) -> Account:
    """Return an account or raise a friendly custom exception."""
    account = accounts.get(account_id)
    if account is None:
        raise AccountNotFoundError(f"Account {account_id} not found.")
    return account


def _validate_amount(amount: float, action: str) -> None:
    if amount <= 0:
        raise InvalidAmountError(f"{action} amount must be positive.")


# ==================== 4. CORE BUSINESS LOGIC ====================
def create_account(name: str) -> Account:
    """Create an account with a unique, never-reused ID."""
    if not name or not name.strip():
        raise ValueError("Customer name cannot be empty.")

    next_id = max(accounts.keys()) + 1 if accounts else 1001
    account = Account(account_id=next_id, name=name.strip(), balance=0.0)
    accounts[next_id] = account
    customer_index[account.name].append(next_id)
    transaction_history[next_id] = []
    return account


def deposit(account_id: int, amount: float) -> float:
    """Deposit money and store it in this account's history."""
    _validate_amount(amount, "Deposit")
    account = _get_account(account_id)
    account.balance += amount
    transaction_history[account_id].append(
        Transaction("Deposit", amount, None, account_id, datetime.now())
    )
    return account.balance


def withdraw(account_id: int, amount: float) -> float:
    """Withdraw money and store it in this account's history."""
    _validate_amount(amount, "Withdrawal")
    account = _get_account(account_id)
    if amount > account.balance:
        raise InsufficientFundsError(
            f"Insufficient Funds. Current balance: Rs.{account.balance:.2f}"
        )

    account.balance -= amount
    transaction_history[account_id].append(
        Transaction("Withdrawal", amount, account_id, None, datetime.now())
    )
    return account.balance


def transfer(from_id: int, to_id: int, amount: float) -> None:
    """Transfer money atomically and record both sides of the transaction."""
    _validate_amount(amount, "Transfer")
    if from_id == to_id:
        raise ValueError("Source and destination accounts must be different.")

    # Validate both accounts before changing any balance.
    source = _get_account(from_id)
    target = _get_account(to_id)
    if amount > source.balance:
        raise InsufficientFundsError(
            f"Insufficient Funds. Current balance: Rs.{source.balance:.2f}"
        )

    source_balance = source.balance
    target_balance = target.balance
    source_history_length = len(transaction_history[from_id])
    target_history_length = len(transaction_history[to_id])
    timestamp = datetime.now()

    try:
        source.balance -= amount
        transaction_history[from_id].append(
            Transaction("Transfer", amount, from_id, to_id, timestamp)
        )

        target.balance += amount
        transaction_history[to_id].append(
            Transaction("Transfer Received", amount, from_id, to_id, timestamp)
        )
    except Exception:
        # Manual rollback: a failed second step restores both accounts exactly.
        source.balance = source_balance
        target.balance = target_balance
        del transaction_history[from_id][source_history_length:]
        del transaction_history[to_id][target_history_length:]
        raise


def reverse_last_transaction(account_id: int) -> bool:
    """Reverse only the latest transaction for the selected account."""
    account = _get_account(account_id)
    history = transaction_history[account_id]
    if not history:
        print("No transaction history available to reverse.")
        return False

    transaction = history[-1]
    if transaction.transaction_type == "Deposit":
        if account.balance < transaction.amount:
            raise InsufficientFundsError(
                "Cannot reverse deposit: the deposited funds have been used."
            )
        account.balance -= transaction.amount
        history.pop()
    elif transaction.transaction_type == "Withdrawal":
        account.balance += transaction.amount
        history.pop()
    elif transaction.transaction_type in ("Transfer", "Transfer Received"):
        _reverse_transfer(account_id, transaction)
    else:
        raise ValueError("Cannot reverse an unknown transaction type.")
    return True


def _reverse_transfer(account_id: int, transaction: Transaction) -> None:
    """Undo both sides of one transfer while maintaining total balance."""
    source = _get_account(transaction.source_account)  # type: ignore[arg-type]
    target = _get_account(transaction.target_account)  # type: ignore[arg-type]

    if target.balance < transaction.amount:
        raise InsufficientFundsError(
            "Cannot reverse transfer: receiving account does not have enough funds."
        )

    target.balance -= transaction.amount
    source.balance += transaction.amount
    transaction_history[account_id].pop()

    counterpart_type = (
        "Transfer Received"
        if transaction.transaction_type == "Transfer"
        else "Transfer"
    )
    other_account_id = (
        transaction.target_account
        if account_id == transaction.source_account
        else transaction.source_account
    )
    other_history = transaction_history[other_account_id]  # type: ignore[index]
    for index in range(len(other_history) - 1, -1, -1):
        item = other_history[index]
        if (
            item.transaction_type == counterpart_type
            and item.amount == transaction.amount
            and item.source_account == transaction.source_account
            and item.target_account == transaction.target_account
            and item.timestamp == transaction.timestamp
        ):
            other_history.pop(index)
            break


def check_balance(account_id: int) -> Account:
    """Fetch account for inquiry using an O(1) dictionary lookup."""
    return _get_account(account_id)


def find_accounts_by_name(name: str) -> List[Account]:
    """Find all accounts for one name via the secondary index."""
    return [accounts[account_id] for account_id in customer_index.get(name.strip(), [])]


def close_account(account_id: int) -> bool:
    """Remove account from the ledger and its secondary index."""
    account = _get_account(account_id)
    customer_index[account.name].remove(account_id)
    if not customer_index[account.name]:
        del customer_index[account.name]
    del transaction_history[account_id]
    del accounts[account_id]
    return True


# ==================== 5. MENU AND MAIN LOOP ====================
def display_menu() -> None:
    print("\n========= SecureBank =========")
    print("1 Create Account")
    print("2 Deposit")
    print("3 Withdraw")
    print("4 Check Balance")
    print("5 Close Account")
    print("6 Transfer Money")
    print("7 Reverse Last Transaction")
    print("8 Find Customer Accounts")
    print("9 Exit")
    print("==============================")


def main() -> None:
    while True:
        display_menu()
        choice = input("Choose : ").strip()

        try:
            if choice == "1":
                name = input("Enter Customer Name: ").strip()
                account = create_account(name)
                print("\nAccount Created Successfully")
                print(f"ID : {account.account_id}")
                print(f"Name : {account.name}")
                print(f"Balance : Rs.{account.balance:.2f}")

            elif choice == "2":
                account_id = int(input("Enter Account ID: ").strip())
                amount = float(input("Enter Amount: ").strip())
                new_balance = deposit(account_id, amount)
                print(f"\nRs.{amount:.2f} deposited successfully.")
                print(f"Current Balance: Rs.{new_balance:.2f}")

            elif choice == "3":
                account_id = int(input("Enter Account ID: ").strip())
                amount = float(input("Enter Amount: ").strip())
                new_balance = withdraw(account_id, amount)
                print("\nWithdrawal Successful")
                print(f"Balance: Rs.{new_balance:.2f}")

            elif choice == "4":
                account = check_balance(int(input("Enter Account ID: ").strip()))
                print(f"\nName : {account.name}")
                print(f"Balance : Rs.{account.balance:.2f}")

            elif choice == "5":
                close_account(int(input("Enter Account ID: ").strip()))
                print("\nAccount Closed Successfully")

            elif choice == "6":
                from_id = int(input("Enter Source Account ID: ").strip())
                to_id = int(input("Enter Destination Account ID: ").strip())
                amount = float(input("Enter Amount: ").strip())
                transfer(from_id, to_id, amount)
                print("\nTransfer Successful")

            elif choice == "7":
                account_id = int(input("Enter Account ID: ").strip())
                if reverse_last_transaction(account_id):
                    print("Last transaction reversed successfully.")

            elif choice == "8":
                name = input("Enter Customer Name: ").strip()
                results = find_accounts_by_name(name)
                if not results:
                    print("No accounts found for this customer.")
                else:
                    for account in results:
                        print(
                            f"ID : {account.account_id}, "
                            f"Name : {account.name}, "
                            f"Balance : Rs.{account.balance:.2f}"
                        )

            elif choice == "9":
                print("\nExiting SecureBank. Goodbye!")
                break

            else:
                print("Invalid choice. Please select 1-9.")

        except (ValueError, AccountNotFoundError, InvalidAmountError, InsufficientFundsError) as error:
            print(f"Error: {error}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
