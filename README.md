# 🏦 SecureBank - Console Banking Application

**Week 1 • Account Fundamentals • In-Memory Ledger**

A pure-Python, menu-driven banking system built from absolute zero. No databases, no JSON, no external libraries—just Python fundamentals (dictionaries, dataclasses, and custom exceptions). Perfectly validates all inputs and never crashes with a traceback.

---

## ✨ Features

| Operation | Description |
| :--- | :--- |
| **1. Create Account** | User enters a name; system auto-generates a unique `Account ID` (starting at 1001, never reused) with a `₹0` balance. |
| **2. Deposit** | Add positive funds to an existing account. Rejects `0` or negative amounts. |
| **3. Withdraw** | Remove funds if the amount is positive and less than or equal to the current balance. |
| **4. Balance Inquiry** | Display the account holder's name and current balance. |
| **5. Close Account** | Permanently remove the account from the system. Any future operation on this ID fails gracefully with "Account Not Found". |
| **6. Exit** | Terminates the program safely. |

---

## 🧠 How It Works (Core Design)

- **Hashmap (Dictionary) Backend**:  
  All accounts are stored in a single `dict[int, Account]`. This provides **O(1)** average lookup time for deposits, withdrawals, and balance checks—exactly as the specification demands.

- **`@dataclass` Account Model**:  
  Every account is a lightweight dataclass storing `account_id`, `customer_name`, and `balance`.

- **Custom Exceptions**:  
  Instead of raising generic `Exception`, we use:
  - `AccountNotFoundError`
  - `InsufficientFundsError`
  - `InvalidAmountError`  
  This keeps the business logic clean and allows the UI to display user‑friendly messages instead of raw Python errors.

- **Never‑Reuse IDs**:  
  When creating a new account, the system looks at the current maximum ID and increments it by 1 (`max(accounts.keys()) + 1`). Even if an account is closed, its ID will never be assigned to another customer.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+ (for `@dataclass` support)

### Installation
1. Clone or download this repository.
2. Ensure the following file is in your working directory:
    bank_console.py

### Running the Application
Open your terminal and run:
```bash
python bank_console.py