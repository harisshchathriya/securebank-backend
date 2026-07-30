from dataclasses import dataclass

# ==================== 1. CUSTOM EXCEPTIONS ====================
class AccountNotFoundError(Exception):
    """Raised when account ID doesn't exist."""
    pass

class InsufficientFundsError(Exception):
    """Raised when withdrawal exceeds balance."""
    pass

class InvalidAmountError(Exception):
    """Raised when amount is <= 0."""
    pass

# ==================== 2. ACCOUNT DATACLASS ====================
@dataclass
class Account:
    account_id: int
    name: str
    balance: float = 0.0

# ==================== 3. IN-MEMORY LEDGER (HASHMAP/DICT) ====================
accounts: dict[int, Account] = {}

# ==================== 4. CORE BUSINESS LOGIC ====================

def create_account(name: str) -> Account:
    """Creates account. Automatically generates unique, never-reused ID."""
    if not name or not name.strip():
        raise ValueError("Customer name cannot be empty.")
    
    # TRAP PREVENTED: Never reuse IDs after closure.
    # We use max() to always jump to the highest number + 1.
    next_id = max(accounts.keys()) + 1 if accounts else 1001
    
    account = Account(account_id=next_id, name=name.strip(), balance=0.0)
    accounts[next_id] = account
    return account

def deposit(account_id: int, amount: float) -> float:
    """Deposits money. Rejects <= 0. Uses dict O(1) lookup."""
    # TRAP PREVENTED: Negative or zero deposits rejected.
    if amount <= 0:
        raise InvalidAmountError("Deposit amount must be positive.")
    
    # TRAP PREVENTED: Checking membership BEFORE accessing to avoid KeyError.
    account = accounts.get(account_id)
    if account is None:
        raise AccountNotFoundError(f"Account {account_id} not found.")
    
    account.balance += amount
    return account.balance

def withdraw(account_id: int, amount: float) -> float:
    """Withdraws money. Rejects <= 0 and over-withdrawal."""
    # TRAP PREVENTED: Negative or zero withdrawals rejected.
    if amount <= 0:
        raise InvalidAmountError("Withdrawal amount must be positive.")
    
    # TRAP PREVENTED: Membership check to avoid KeyError crash.
    account = accounts.get(account_id)
    if account is None:
        raise AccountNotFoundError(f"Account {account_id} not found.")
    
    # TRAP PREVENTED: Over-withdrawal rejected with clear message (not a traceback).
    if amount > account.balance:
        raise InsufficientFundsError(
            f"Insufficient Funds. Current balance: ₹{account.balance}"
        )
    
    account.balance -= amount
    return account.balance

def check_balance(account_id: int) -> Account:
    """Fetches account for inquiry. Uses dict O(1) lookup."""
    account = accounts.get(account_id)
    if account is None:
        raise AccountNotFoundError(f"Account {account_id} not found.")
    return account

def close_account(account_id: int) -> bool:
    """Removes account from dict (hashmap deletion)."""
    # TRAP PREVENTED: Checks existence before deleting to avoid KeyError.
    if account_id not in accounts:
        raise AccountNotFoundError(f"Account {account_id} not found.")
    
    del accounts[account_id]  # O(1) hashmap deletion
    return True

# ==================== 5. MENU AND MAIN LOOP ====================

def display_menu():
    print("\n========= SecureBank =========")
    print("1 Create Account")
    print("2 Deposit")
    print("3 Withdraw")
    print("4 Check Balance")
    print("5 Close Account")
    print("6 Exit")
    print("==============================")

def main():
    while True:
        display_menu()
        choice = input("Choose : ").strip()

        # --- 1. CREATE ---
        if choice == '1':
            name = input("Enter Customer Name: ").strip()
            if not name:
                print("Name cannot be empty.")
            else:
                try:
                    acc = create_account(name)
                    print("\nAccount Created Successfully")
                    print(f"ID : {acc.account_id}")
                    print(f"Name : {acc.name}")
                    print(f"Balance : ₹{acc.balance}")
                except Exception as e:
                    print(f"Error: {e}")

        # --- 2. DEPOSIT ---
        elif choice == '2':
            try:
                acc_id = int(input("Enter Account ID: ").strip())
                amt = float(input("Enter Amount: ").strip())
                new_bal = deposit(acc_id, amt)
                print(f"\n₹{amt} deposited successfully.")
                print(f"Current Balance: ₹{new_bal}")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            except (AccountNotFoundError, InvalidAmountError) as e:
                print(e)  # Friendly message, no traceback.

        # --- 3. WITHDRAW ---
        elif choice == '3':
            try:
                acc_id = int(input("Enter Account ID: ").strip())
                amt = float(input("Enter Amount: ").strip())
                new_bal = withdraw(acc_id, amt)
                print("\nWithdrawal Successful")
                print(f"Balance: ₹{new_bal}")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            except (AccountNotFoundError, InvalidAmountError, InsufficientFundsError) as e:
                print(e)  # Friendly message, no traceback.

        # --- 4. BALANCE INQUIRY ---
        elif choice == '4':
            try:
                acc_id = int(input("Enter Account ID: ").strip())
                acc = check_balance(acc_id)
                print(f"\nName : {acc.name}")
                print(f"Balance : ₹{acc.balance}")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            except AccountNotFoundError as e:
                print(e)

        # --- 5. CLOSE ACCOUNT ---
        elif choice == '5':
            try:
                acc_id = int(input("Enter Account ID: ").strip())
                close_account(acc_id)
                print("\nAccount Closed Successfully")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            except AccountNotFoundError as e:
                print(e)

        # --- 6. EXIT ---
        elif choice == '6':
            print("\nExiting SecureBank. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-6.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()