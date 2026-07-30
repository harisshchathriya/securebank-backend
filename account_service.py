from account import Account
from exceptions import AccountNotFoundError, InsufficientFundsError, InvalidAmountError

# In‑memory store – dictionary with account_id as key
accounts: dict[int, Account] = {}

# ------------------- Core Operations -------------------

def create_account(name: str) -> Account:
    """Create a new account with auto‑generated ID and zero balance."""
    if not name or not name.strip():
        raise ValueError("Customer name cannot be empty.")
    
    # Generate next ID: start at 1001, increment from max existing
    next_id = max(accounts.keys()) + 1 if accounts else 1001
    account = Account(account_id=next_id, name=name.strip(), balance=0)
    accounts[next_id] = account
    return account

def deposit(account_id: int, amount: float) -> int:
    """Deposit a positive amount into the account. Returns new balance."""
    if amount <= 0:
        raise InvalidAmountError("Deposit amount must be positive.")
    account = accounts.get(account_id)
    if account is None:
        raise AccountNotFoundError(f"Account {account_id} not found.")
    amt = int(amount)
    if amt <= 0:
        raise InvalidAmountError("Deposit amount must be a positive integer.")
    account.balance += amt
    return account.balance

def withdraw(account_id: int, amount: float) -> int:
    """Withdraw a positive amount if sufficient balance. Returns new balance."""
    if amount <= 0:
        raise InvalidAmountError("Withdrawal amount must be positive.")
    account = accounts.get(account_id)
    if account is None:
        raise AccountNotFoundError(f"Account {account_id} not found.")
    amt = int(amount)
    if amt > account.balance:
        raise InsufficientFundsError(
            f"Insufficient funds. Current balance: ₹{account.balance}"
        )
    if amt <= 0:
        raise InvalidAmountError("Withdrawal amount must be a positive integer.")
    account.balance -= amt
    return account.balance

def check_balance(account_id: int) -> Account:
    """Retrieve account details for balance inquiry."""
    account = accounts.get(account_id)
    if account is None:
        raise AccountNotFoundError(f"Account {account_id} not found.")
    return account

def close_account(account_id: int) -> bool:
    """Remove the account from the store. Returns True on success."""
    if account_id not in accounts:
        raise AccountNotFoundError(f"Account {account_id} not found.")
    del accounts[account_id]
    return True

# Optional helper – not required by specs but may be useful
def get_all_accounts() -> dict[int, Account]:
    """Return the entire accounts dictionary (read‑only)."""
    return accounts