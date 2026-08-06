# 🏦 SecureBank - Console Banking Application

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)
![Status](https://img.shields.io/badge/Status-Week%201-success)
![License](https://img.shields.io/badge/License-Educational-green)

## 📌 Overview

**SecureBank** is a console-based banking application developed in Python as part of a structured backend development roadmap. The project focuses on implementing fundamental banking operations while strengthening core Python programming concepts such as dictionaries, functions, exception handling, and object-oriented programming.

This project is implemented using **pure Python**, without databases or external libraries, making it an excellent demonstration of backend programming fundamentals.

---

# ✨ Features

- ✅ Create Account
- ✅ Deposit Money
- ✅ Withdraw Money
- ✅ Check Account Balance
- ✅ Close Account
- ✅ Input Validation
- ✅ Custom Exception Handling
- ✅ Menu-Driven Interface
- ✅ Automatic Account ID Generation
- ✅ Safe Program Execution (No Tracebacks)

---

# 🧠 Core Design

## 🔹 In-Memory Ledger

All accounts are stored inside a Python dictionary.

```python
accounts = {
    1001: Account(...),
    1002: Account(...),
}
```

Using a dictionary provides **O(1)** average lookup time for account operations.

---

## 🔹 Account Model

Each account stores:

- Account ID
- Customer Name
- Balance

---

## 🔹 Custom Exceptions

The application handles invalid operations gracefully using custom exceptions.

- AccountNotFoundError
- InsufficientFundsError
- InvalidAmountError

Instead of displaying Python tracebacks, the application provides user-friendly error messages.

---

## 🔹 Unique Account IDs

Account IDs begin from **1001** and increase automatically.

Closed account IDs are **never reused**, ensuring uniqueness.

---

# 🛠 Technologies Used

- Python 3
- Git
- GitHub
- VS Code

---

# 📚 Python Concepts Demonstrated

- Variables
- Functions
- Loops
- Conditional Statements
- Dictionaries
- Object-Oriented Programming
- Dataclasses
- Exception Handling
- CRUD Operations
- Input Validation
- Modular Programming

---

# 📂 Project Structure

```
SecureBank/
│
├── bank_console.py
├── README.md
└── .gitignore
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.7 or above

---

## Installation

Clone the repository:

```bash
git clone https://github.com/harisshchathriya/securebank-backend.git
```

Navigate into the project:

```bash
cd securebank-backend
```

---

## ▶️ Running the Application

Run the program:

```bash
python bank_console.py
```

or

```bash
py bank_console.py
```

---

# 📷 Console Preview

```text
========= SecureBank =========

1. Create Account
2. Deposit
3. Withdraw
4. Check Balance
5. Close Account
6. Exit

Choose:
```

*(Replace this section later with an actual screenshot of your running application.)*

---

# ✅ Sample Workflow

```text
Create Account
        │
        ▼
Deposit Money
        │
        ▼
Withdraw Money
        │
        ▼
Check Balance
        │
        ▼
Close Account
```

---

# 🚀 Future Enhancements

This project is part of a larger backend development roadmap.

Future versions will include:

- Money Transfer
- Transaction History
- JSON File Storage
- FastAPI REST API
- SQLAlchemy ORM
- SQLite / PostgreSQL
- JWT Authentication
- Role-Based Authorization (RBAC)
- Automated Testing (PyTest)
- Docker Deployment

---

# 🎯 Learning Objectives

This project was built to strengthen knowledge in:

- Python Fundamentals
- Backend Development
- Object-Oriented Programming
- Exception Handling
- Clean Code Practices
- Data Structures
- Problem Solving
- Software Design

---

# 📈 Repository Roadmap

| Week | Topic | Status |
|------|-----------------------------|--------|
| Week 1 | Account Fundamentals | ✅ Completed |
| Week 2 | Money Transfer | ⏳ Planned |
| Week 3 | Transaction History | ⏳ Planned |
| Week 4 | JSON Persistence | ⏳ Planned |
| Week 5 | FastAPI | ⏳ Planned |
| Week 6 | Layered Architecture | ⏳ Planned |
| Week 7 | SQLAlchemy | ⏳ Planned |
| Week 8 | Validation | ⏳ Planned |
| Week 9 | Authentication | ⏳ Planned |
| Week 10 | JWT | ⏳ Planned |
| Week 11 | RBAC | ⏳ Planned |
| Week 12 | Testing | ⏳ Planned |
| Week 13 | API Documentation | ⏳ Planned |
| Week 14 | Docker Deployment | ⏳ Planned |

---

# 👨‍💻 Author

**Harissh Chathriya**

B.Tech – Artificial Intelligence & Data Science

GitHub:
https://github.com/harisshchathriya

---

# 📄 License

This project is created for educational and learning purposes.

---

⭐ If you found this project useful, consider giving the repository a star.