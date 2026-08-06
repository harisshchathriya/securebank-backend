# bank_console.py – Day 1: Account Fundamentals
# Create, deposit, withdraw, balance, close

from dataclasses import dataclass
from typing import Dict, Optional
import sys

# ---------- Custom Exceptions ----------
class AccountNotFoundError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class InvalidAmountError(Exception):
    pass

# ---------- Data Models ----------
@dataclass
class Account:
    id: int
    customer_name: str
    balance: float = 0.0

# ---------- The Ledger ----------
accounts: Dict[int, Account] = {}
next_account_id = 1

# ---------- Core Functions ----------
def _get_account(account_id: int) -> Account:
    if account_id not in accounts:
        raise AccountNotFoundError(f"Account {account_id} does not exist.")
    return accounts[account_id]

def create_account(customer_name: str, initial_balance: float = 0.0) -> Account:
    if initial_balance < 0:
        raise InvalidAmountError("Initial balance cannot be negative.")
    global next_account_id
    acc = Account(id=next_account_id, customer_name=customer_name, balance=initial_balance)
    accounts[next_account_id] = acc
    next_account_id += 1
    return acc

def deposit(account_id: int, amount: float) -> None:
    if amount <= 0:
        raise InvalidAmountError("Deposit amount must be positive.")
    acc = _get_account(account_id)
    acc.balance += amount

def withdraw(account_id: int, amount: float) -> None:
    if amount <= 0:
        raise InvalidAmountError("Withdrawal amount must be positive.")
    acc = _get_account(account_id)
    if acc.balance < amount:
        raise InsufficientFundsError(f"Insufficient balance. Available: {acc.balance:.2f}")
    acc.balance -= amount

def get_balance(account_id: int) -> float:
    return _get_account(account_id).balance

def close_account(account_id: int) -> None:
    acc = _get_account(account_id)
    if acc.balance != 0:
        raise ValueError("Cannot close account with non-zero balance.")
    del accounts[account_id]

# ---------- CLI Menu ----------
def print_menu():
    print("\n" + "="*50)
    print("SECUREBANK – DAY 1 (BASICS)")
    print("1. Create account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check balance")
    print("5. Close account")
    print("6. Show all accounts (debug)")
    print("0. Exit")
    print("="*50)

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        try:
            if choice == "1":
                name = input("Customer name: ").strip()
                if not name:
                    print("Name cannot be empty.")
                    continue
                init_bal = float(input("Initial balance (0 if none): ") or "0")
                acc = create_account(name, init_bal)
                print(f"Account created with ID {acc.id}, balance {acc.balance:.2f}")

            elif choice == "2":
                acc_id = int(input("Account ID: "))
                amount = float(input("Amount to deposit: "))
                deposit(acc_id, amount)
                print(f"Deposit successful. New balance: {get_balance(acc_id):.2f}")

            elif choice == "3":
                acc_id = int(input("Account ID: "))
                amount = float(input("Amount to withdraw: "))
                withdraw(acc_id, amount)
                print(f"Withdrawal successful. New balance: {get_balance(acc_id):.2f}")

            elif choice == "4":
                acc_id = int(input("Account ID: "))
                print(f"Balance: {get_balance(acc_id):.2f}")

            elif choice == "5":
                acc_id = int(input("Account ID: "))
                close_account(acc_id)
                print(f"Account {acc_id} closed successfully.")

            elif choice == "6":
                print("\n--- ALL ACCOUNTS ---")
                for acc in accounts.values():
                    print(f"ID: {acc.id}, Name: {acc.customer_name}, Balance: {acc.balance:.2f}")
                print("--- END ---")

            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

        except (AccountNotFoundError, InsufficientFundsError, InvalidAmountError, ValueError) as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()