import pandas as pd

transactions = []
categories = ["food", "transport", "other"]
budget = 100.0
filename = "transactions.txt"

def load_transactions():
    try:
        with open(filename, "r") as file:
            for line in file:
                amount, category = line.strip().split(",")
                transactions.append({"amount": float(amount), "category": category})
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error loading transactions: {e}")

def save_transactions():
    try:
        with open(filename, "w") as file:
            for transaction in transactions:
                file.write(f"{transaction['amount']},{transaction['category']}\n")
    except Exception as e:
        print(f"Error saving transactions: {e}")

def add_transaction():
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be positive.")
           
        category = input("Enter category (food, transport, other): ").lower()
        if category not in categories:
            print("Invalid category. Choose food, transport, or other.")
           
        transaction = {"amount": amount, "category": category}
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
        
    print("\nTransaction History:")
    print("Amount | Category")
    print("----------------")
    total = 0
    for transaction in transactions:
        amount = transaction["amount"]
        category = transaction["category"]
        print(f"${amount:.2f} | {category}")
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
        
    df = pd.DataFrame(transactions)
    summary = df.groupby("category")["amount"].sum()
    print("\nSpending by Category:")
    print(summary)
    print(f"\nTotal Spending: ${df['amount'].sum():.2f}")

def main():
    load_transactions()
    while True:
        print("\n=== Simple Expense Tracker ===")
        print("1. Add Transaction")
        print("2. View History")
        print("3. View Summary by Category")
        print("4. Exit")
        try:
            choice = input("Enter choice (1-4): ")
            if choice == "1":
                add_transaction()
            elif choice == "2":
                view_history()
            elif choice == "3":
                view_summary()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
        except EOFError:
            print("Input interrupted. Exiting program.")
            break
        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting.")
            break

if __name__ == "__main__":
    main()