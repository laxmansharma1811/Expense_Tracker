Simple Expense Tracker
A command-line Python application to manage personal expenses. Track transactions, categorize spending, monitor a budget, and summarize expenses by category. Ideal for beginners learning Python concepts like variables, lists, dictionaries, functions, file I/O, error handling, and Pandas.
Features

Add Transactions: Record expenses with an amount and category (food, transport, other).
View History: See all transactions, total spending, and budget status.
Category Summary: View spending per category using Pandas.
Budget Tracking: Set a total budget and get warnings if exceeded.
Data Persistence: Save transactions to transactions.txt for reuse.
Robust Error Handling: Manages invalid inputs and interruptions.

Prerequisites

Python 3.6+
Pandas (installed via pip)
A terminal or command-line interface

Installation

Clone the Repository:
git clone <repository-url>
cd expense-tracker


Set Up a Virtual Environment:
python -m venv .venv

Activate it:

Windows:.venv\Scripts\activate


macOS/Linux:source .venv/bin/activate




Install Dependencies:
pip install pandas

Or use requirements.txt if provided:
pip install -r requirements.txt



Usage

Run the Application:
python expense_tracker.py


Navigate the Menu:

1. Add Transaction: Input an amount and category.
2. View History: Display transactions and budget details.
3. View Summary by Category: Show spending per category.
4. Exit: Close the program.


Example:
=== Simple Expense Tracker ===
1. Add Transaction
2. View History
3. View Summary by Category
4. Exit
Enter choice (1-4): 1
Enter amount: 25
Enter category (food, transport, other): transport
Transaction added!

Enter choice (1-4): 3
Spending by Category:
category
transport    25.0
Name: amount, dtype: float64

Total Spending: $25.00


Transaction Storage:Transactions are saved in transactions.txt:
25.0,transport



Project Structure
expense-tracker/
├── .gitignore          # Excludes .venv/, transactions.txt, etc.
├── expense_tracker.py  # Main script
├── README.md           # This file
├── requirements.txt    # Dependencies (optional)
├── transactions.txt    # Data file (git-ignored)
└── .venv/             # Virtual environment (git-ignored)

Contributing

Fork the repository.
Create a branch:git checkout -b feature/your-feature


Commit changes:git commit -m "Add your feature"


Push to your fork:git push origin feature/your-feature


Submit a pull request.

License
MIT License (see LICENSE file for details).
Future Improvements

Add transaction dates.
Support per-category budgets.
Allow editing or deleting transactions.
Export summaries to CSV.

Contact
For questions or suggestions, open an issue on the GitHub repository.
