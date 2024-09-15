import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Initialize the database
def init_db():
    with sqlite3.connect('budget.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT,
                        amount REAL,
                        description TEXT
                    )''')
        conn.commit()

# Add a transaction to the database
def add_transaction(type_, amount, description):
    with sqlite3.connect('budget.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO transactions (type, amount, description) VALUES (?, ?, ?)', 
                  (type_, amount, description))
        conn.commit()

# Fetch all transactions from the database
def fetch_transactions():
    with sqlite3.connect('budget.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM transactions')
        return c.fetchall()

# Main application class
class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Budget Tracker")
        self.create_widgets()

    def create_widgets(self):
        # Input Form
        self.type_label = tk.Label(self.root, text="Type")
        self.type_label.grid(row=0, column=0, padx=10, pady=10)
        self.type_var = tk.StringVar()
        self.type_income = tk.Radiobutton(self.root, text="Income", variable=self.type_var, value="Income")
        self.type_expense = tk.Radiobutton(self.root, text="Expense", variable=self.type_var, value="Expense")
        self.type_income.grid(row=0, column=1, padx=10, pady=10)
        self.type_expense.grid(row=0, column=2, padx=10, pady=10)

        self.amount_label = tk.Label(self.root, text="Amount")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

        self.description_label = tk.Label(self.root, text="Description")
        self.description_label.grid(row=2, column=0, padx=10, pady=10)
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Transactions Table
        self.tree = ttk.Treeview(self.root, columns=("ID", "Type", "Amount", "Description"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.load_transactions()

    def add_transaction(self):
        type_ = self.type_var.get()
        amount = self.amount_entry.get()
        description = self.description_entry.get()
        
        if not (type_ and amount):
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")
            return

        add_transaction(type_, amount, description)
        self.clear_inputs()
        self.load_transactions()

    def load_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        transactions = fetch_transactions()
        for transaction in transactions:
            self.tree.insert('', 'end', values=transaction)

    def clear_inputs(self):
        self.type_var.set('')
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
