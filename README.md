Simple Expense Tracker
A command-line application built with Python to track expenses, categorize transactions, set a budget, and summarize spending. This project is designed for beginners learning Python fundamentals, including variables, data structures, functions, file I/O, error handling, and Pandas for data analysis.
Features

Add Transactions: Record expenses with an amount and category (e.g., food, transport, other).
View Transaction History: Display all transactions with total spending and budget status.
Summarize by Category: Use Pandas to show spending per category.
Budget Tracking: Set a total budget and receive warnings if exceeded.
Persistent Storage: Save transactions to a text file (transactions.txt) for persistence across sessions.
Error Handling: Handle invalid inputs and interruptions (e.g., EOFError, KeyboardInterrupt).

Prerequisites

Python 3.x: Ensure Python 3.6 or higher is installed (Download Python).
Pandas: Required for category summarization (installed via pip).
A terminal or command-line interface to run the program.

Setup

Clone the Repository:
git clone <repository-url>
cd expense-tracker


Create a Virtual Environment:
python -m venv .venv

Activate the virtual environment:

On Windows:.venv\Scripts\activate


On macOS/Linux:source .venv/bin/activate




Install Dependencies:Install Pandas using the provided requirements.txt (if included) or manually:
pip install pandas

Or, if requirements.txt is present:
pip install -r requirements.txt



Usage

Run the Program:
python expense_tracker.py


Menu Options:

1. Add Transaction: Enter an amount and category to record an expense.
2. View History: Display all transactions, total spending, and budget status.
3. View Summary by Category: Show spending per category using Pandas.
4. Exit: Quit the program.


Example Interaction:
=== Simple Expense Tracker ===
1. Add Transaction
2. View History
3. View Summary by Category
4. Exit
Enter choice (1-4): 1
Enter amount: 50
Enter category (food, transport, other): food
Transaction added!

Enter choice (1-4): 2
Transaction History:
Amount | Category
----------------
$50.00 | food

Total Spending: $50.00
Budget: $100.00
Remaining Budget: $50.00


Data Storage:

Transactions are saved to transactions.txt in the project directory.
Example content:50.0,food
20.0,transport





Project Structure
expense-tracker/
├── .gitignore          # Ignores .venv/, transactions.txt, etc.
├── expense_tracker.py  # Main Python script
├── requirements.txt    # Dependency list (optional)
├── transactions.txt    # Transaction data (ignored)
└── .venv/             # Virtual environment (ignored)

Contributing

Fork the repository.
Create a new branch:git checkout -b feature/your-feature


Make changes and commit:git commit -m "Add your feature"


Push to your fork:git push origin feature/your-feature


Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built as part of a Python fundamentals learning exercise.
Uses Pandas for data summarization.

