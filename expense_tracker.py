import pandas as pd
import uuid

transactions = []
loans = []
categories = ["food", "transport", "other"]
budget = 100.0
transactions_filename = "transactions.csv"
users_filename = "users.csv"
loans_filename = "loans.csv"
current_user = None

def load_users():
    try:
        df = pd.read_csv(users_filename)
        users = df.to_dict('records')
        for user in users:
            user['username'] = str(user['username'])
            user['password'] = str(user['password'])
        return users
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading users: {e}")
        return []

def save_users(users):
    try:
        df = pd.DataFrame(users)
        df.to_csv(users_filename, index=False)
    except Exception as e:
        print(f"Error saving users: {e}")

def register_user():
    users = load_users()
    username = input("Enter new username: ").strip()
    if any(user['username'] == username for user in users):
        print("Username already exists.")
        return False
    password = input("Enter password: ").strip()
    if not username or not password:
        print("Username and password cannot be empty.")
        return False
    users.append({"username": username, "password": password})
    save_users(users)
    users = load_users()
    if any(user['username'] == username for user in users):
        print("User registered successfully!")
        return True
    else:
        print("Failed to register user. Please try again.")
        return False

def login():
    global current_user
    users = load_users()
    if not users:
        print("No users found. Please register first.")
        return False
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    for user in users:
        if user['username'] == username and user['password'] == password:
            current_user = username
            print(f"Welcome, {username}!")
            return True
    print("Invalid username or password.")
    return False

def load_transactions():
    global transactions
    try:
        df = pd.read_csv(transactions_filename)
        transactions = df.to_dict('records')
        for t in transactions:
            t['amount'] = float(t['amount'])
            t['category'] = str(t['category'])
            t['user'] = str(t['user'])
        if current_user:
            transactions = [t for t in transactions if t['user'] == current_user]
    except FileNotFoundError:
        transactions = []
    except Exception as e:
        print(f"Error loading transactions: {e}")

def save_transactions():
    try:
        all_transactions = []
        try:
            df = pd.read_csv(transactions_filename)
            all_transactions = df.to_dict('records')
        except FileNotFoundError:
            pass
        all_transactions = [t for t in all_transactions if t['user'] != current_user]
        all_transactions.extend(transactions)
        df = pd.DataFrame(all_transactions)
        df.to_csv(transactions_filename, index=False)
    except Exception as e:
        print(f"Error saving transactions: {e}")

def load_loans():
    global loans
    try:
        df = pd.read_csv(loans_filename)
        loans = df.to_dict('records')
        for loan in loans:
            loan['amount'] = float(loan['amount'])
            loan['interest_rate'] = float(loan['interest_rate'])
            loan['user'] = str(loan['user'])
            loan['loan_id'] = str(loan['loan_id'])
        if current_user:
            loans = [loan for loan in loans if loan['user'] == current_user]
    except FileNotFoundError:
        loans = []
    except Exception as e:
        print(f"Error loading loans: {e}")

def save_loans():
    try:
        all_loans = []
        try:
            df = pd.read_csv(loans_filename)
            all_loans = df.to_dict('records')
        except FileNotFoundError:
            pass
        all_loans = [loan for loan in all_loans if loan['user'] != current_user]
        all_loans.extend(loans)
        df = pd.DataFrame(all_loans)
        df.to_csv(loans_filename, index=False)
    except Exception as e:
        print(f"Error saving loans: {e}")

def check_budget(amount):
    total_spending = sum(t['amount'] for t in transactions)
    return (budget - total_spending) >= amount

def take_loan(required_amount):
    try:
        print(f"Insufficient budget. Required: ${required_amount:.2f}")
        choice = input("Would you like to take a loan? (yes/no): ").lower().strip()
        if choice != 'yes':
            print("Transaction cancelled.")
            return False
        loan_amount = float(input("Enter loan amount: "))
        if loan_amount <= 0:
            print("Loan amount must be positive.")
            return False
        if loan_amount < required_amount:
            print(f"Loan amount must be at least ${required_amount:.2f}.")
            return False
        interest_rate = 0.05  # 5% simple interest
        loan_id = str(uuid.uuid4())
        loan = {
            "loan_id": loan_id,
            "amount": loan_amount,
            "interest_rate": interest_rate,
            "user": current_user
        }
        loans.append(loan)
        save_loans()
        global budget
        budget += loan_amount
        print(f"Loan of ${loan_amount:.2f} approved at {interest_rate*100:.1f}% interest.")
        return True
    except ValueError:
        print("Invalid input. Loan cancelled.")
        return False
    except EOFError:
        print("Input interrupted. Loan cancelled.")
        return False

def add_transaction():
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        print("\nSelect category:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.capitalize()}")
        category_choice = input("Enter choice (1-3): ").strip()
        if category_choice not in ['1', '2', '3']:
            print("Invalid choice. Please enter 1, 2, or 3.")
            return
        category = categories[int(category_choice) - 1]
        if not check_budget(amount):
            if not take_loan(amount):
                return
        transaction = {"amount": amount, "category": category, "user": current_user}
        transactions.append(transaction)
        save_transactions()
        print("Transaction added!")
    except ValueError:
        print("Invalid amount. Please enter a number.")
    except EOFError:
        print("Input interrupted. Returning to menu.")

def view_history():
    if not transactions:
        print("No transactions found.")
    else:
        print("\nTransaction History:")
        print("Amount | Category | User")
        print("-------------------------")
        total = 0
        for transaction in transactions:
            amount = transaction["amount"]
            category = transaction["category"]
            user = transaction["user"]
            print(f"${amount:.2f} | {category} | {user}")
            total += amount
        print(f"\nTotal Spending: ${total:.2f}")
        print(f"Budget: ${budget:.2f}")
        if total > budget:
            print("Warning: You have exceeded your budget!")
        else:
            print(f"Remaining Budget: ${budget - total:.2f}")

    if not loans:
        print("\nNo loans taken.")
    else:
        print("\nLoan History:")
        print("Loan ID | Amount | Interest Rate | User")
        print("-------------------------------------")
        total_loan = 0
        for loan in loans:
            amount = loan["amount"]
            interest_rate = loan["interest_rate"]
            loan_id = loan["loan_id"]
            user = loan["user"]
            print(f"{loan_id[:8]}... | ${amount:.2f} | {interest_rate*100:.1f}% | {user}")
            total_loan += amount
        print(f"\nTotal Loan Amount: ${total_loan:.2f}")

def view_summary():
    if not transactions:
        print("No transactions found.")
        return
    df = pd.DataFrame(transactions)
    summary = df.groupby("category")["amount"].sum()
    print("\nSpending by Category:")
    print(summary)
    print(f"\nTotal Spending: ${df['amount'].sum():.2f}")
    if loans:
        df_loans = pd.DataFrame(loans)
        total_loan = df_loans["amount"].sum()
        print(f"\nTotal Loans: ${total_loan:.2f}")

def adjust_budget():
    global budget
    try:
        new_budget = float(input("Enter new budget amount: "))
        if new_budget <= 0:
            print("Budget must be positive.")
            return
        budget = new_budget
        print(f"Budget updated to ${budget:.2f}!")
    except ValueError:
        print("Invalid amount. Please enter a number.")
    except EOFError:
        print("Input interrupted. Returning to menu.")

def main():
    while True:
        print("\n=== Expense Tracker Login ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        try:
            choice = input("Enter choice (1-3): ")
            if choice == "1":
                if login():
                    load_transactions()
                    load_loans()
                    while True:
                        print("\n=== Simple Expense Tracker ===")
                        print("1. Add Transaction")
                        print("2. View History")
                        print("3. View Summary by Category")
                        print("4. Adjust Budget")
                        print("5. Logout")
                        try:
                            menu_choice = input("Enter choice (1-5): ")
                            if menu_choice == "1":
                                add_transaction()
                            elif menu_choice == "2":
                                view_history()
                            elif menu_choice == "3":
                                view_summary()
                            elif menu_choice == "4":
                                adjust_budget()
                            elif menu_choice == "5":
                                print("Logged out.")
                                break
                            else:
                                print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                        except EOFError:
                            print("Input interrupted. Returning to login.")
                            break
                        except KeyboardInterrupt:
                            print("\nProgram interrupted by user. Returning to login.")
                            break
            elif choice == "2":
                register_user()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except EOFError:
            print("Input interrupted. Exiting program.")
            break
        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting.")
            break

if __name__ == "__main__":
    main()