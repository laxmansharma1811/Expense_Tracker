import pandas as pd

transactions = []
categories = ["food", "transport", "other"]
budget = 100.0
transactions_filename = "transactions.csv"
users_filename = "users.csv"
current_user = None

def load_users():
    try:
        df = pd.read_csv(users_filename)
        users = df.to_dict('records')
        # Ensure username and password are strings
        for user in users:
            user['username'] = str(user['username'])
            user['password'] = str(user['password'])
        # print(f"Loaded users: {users}")  # Debug: Uncomment to verify loaded users
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
        # print(f"Saved users to {users_filename}: {users}")  # Debug: Uncomment to verify saved users
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
    # Verify user was saved
    users = load_users()
    if any(user['username'] == username for user in users):
        print("User registered successfully!")
        return True
    else:
        print("Failed to register user. Please try again.")
        return False

def login():
    global current_user
    users = load_users()  # Reload users to ensure latest data
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
        # Ensure amount is float, category and user are strings
        for t in transactions:
            t['amount'] = float(t['amount'])
            t['category'] = str(t['category'])
            t['user'] = str(t['user'])
        # Filter transactions for current user
        if current_user:
            transactions = [t for t in transactions if t['user'] == current_user]
    except FileNotFoundError:
        transactions = []
    except Exception as e:
        print(f"Error loading transactions: {e}")

def save_transactions():
    try:
        # Load all transactions to preserve other users' data
        all_transactions = []
        try:
            df = pd.read_csv(transactions_filename)
            all_transactions = df.to_dict('records')
        except FileNotFoundError:
            pass
        # Filter out current user's transactions
        all_transactions = [t for t in all_transactions if t['user'] != current_user]
        # Add current user's transactions
        all_transactions.extend(transactions)
        # Save all transactions
        df = pd.DataFrame(all_transactions)
        df.to_csv(transactions_filename, index=False)
    except Exception as e:
        print(f"Error saving transactions: {e}")

def add_transaction():
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        category = input("Enter category (food, transport, other): ").lower()
        if category not in categories:
            print("Invalid category. Choose food, transport, or other.")
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
        return
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

def view_summary():
    if not transactions:
        print("No transactions found.")
        return
    df = pd.DataFrame(transactions)
    summary = df.groupby("category")["amount"].sum()
    print("\nSpending by Category:")
    print(summary)
    print(f"\nTotal Spending: ${df['amount'].sum():.2f}")

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