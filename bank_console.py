from account_service import (
    create_account,
    deposit,
    withdraw,
    check_balance,
    close_account
)
from exceptions import AccountNotFoundError, InsufficientFundsError, InvalidAmountError

def display_menu():
    """Print the main menu."""
    print("\n========= SecureBank =========")
    print("1 Create Account")
    print("2 Deposit")
    print("3 Withdraw")
    print("4 Check Balance")
    print("5 Close Account")
    print("6 Exit")
    print("==============================")

def main():
    """Main program loop."""
    while True:
        display_menu()
        choice = input("Choose : ").strip()

        # ---------- 1. Create Account ----------
        if choice == '1':
            name = input("Enter Customer Name: ").strip()
            if not name:
                print("Name cannot be empty.")
            else:
                try:
                    account = create_account(name)
                    print("\nAccount Created Successfully")
                    print(f"ID : {account.account_id}")
                    print(f"Name : {account.name}")
                    print(f"Balance : ₹{account.balance}")
                except Exception as e:
                    print(f"Error: {e}")

        # ---------- 2. Deposit ----------
        elif choice == '2':
            try:
                acc_id = int(input("Enter Account ID: ").strip())
                amount = float(input("Enter Amount: ").strip())
                new_balance = deposit(acc_id, amount)
                print(f"\n₹{amount} deposited successfully.")
                print(f"Current Balance: ₹{new_balance}")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            except (AccountNotFoundError, InvalidAmountError) as e:
                print(e)
            except Exception as e:
                print(f"Unexpected error: {e}")

        # ---------- 3. Withdraw ----------
        elif choice == '3':
            try:
                acc_id = int(input("Enter Account ID: ").strip())
                amount = float(input("Enter Amount: ").strip())
                new_balance = withdraw(acc_id, amount)
                print("\nWithdrawal Successful")
                print(f"Balance: ₹{new_balance}")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            except (AccountNotFoundError, InvalidAmountError, InsufficientFundsError) as e:
                print(e)
            except Exception as e:
                print(f"Unexpected error: {e}")

        # ---------- 4. Check Balance ----------
        elif choice == '4':
            try:
                acc_id = int(input("Enter Account ID: ").strip())
                account = check_balance(acc_id)
                print(f"\nName : {account.name}")
                print(f"Balance : ₹{account.balance}")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            except AccountNotFoundError as e:
                print(e)
            except Exception as e:
                print(f"Unexpected error: {e}")

        # ---------- 5. Close Account ----------
        elif choice == '5':
            try:
                acc_id = int(input("Enter Account ID: ").strip())
                close_account(acc_id)
                print("\nAccount Closed Successfully")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            except AccountNotFoundError as e:
                print(e)
            except Exception as e:
                print(f"Unexpected error: {e}")

        # ---------- 6. Exit ----------
        elif choice == '6':
            print("\nExiting SecureBank. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-6.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()