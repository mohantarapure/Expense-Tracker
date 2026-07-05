import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE = "expenses.json"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x550")
        self.root.config(bg="#1e1e2f")

        self.expenses = []
        self.load_data()

        self.setup_ui()
        self.update_table()

    def setup_ui(self):
        title = tk.Label(self.root, text="Expense Tracker", font=("Arial", 22, "bold"), bg="#1e1e2f", fg="white")
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack(pady=10)

        self.name_var = tk.StringVar()
        self.amount_var = tk.StringVar()

        tk.Entry(frame, textvariable=self.name_var, width=20).grid(row=0, column=0, padx=5)
        tk.Entry(frame, textvariable=self.amount_var, width=20).grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Add", command=self.add_expense, bg="#4CAF50", fg="white", width=10).grid(row=0, column=2, padx=5)

        # Table
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2a40", foreground="white", rowheight=25, fieldbackground="#2a2a40")

        self.tree = ttk.Treeview(self.root, columns=("Name", "Amount"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Amount", text="Amount")
        self.tree.pack(pady=20)

        tk.Button(self.root, text="Delete Selected", command=self.delete_expense, bg="#e74c3c", fg="white").pack(pady=5)

        self.total_label = tk.Label(self.root, text="Total: ₹0.00", font=("Arial", 14), bg="#1e1e2f", fg="white")
        self.total_label.pack(pady=10)

    def add_expense(self):
        name = self.name_var.get().strip()
        amount = self.amount_var.get().strip()

        if not name or not amount:
            messagebox.showwarning("Error", "Enter all fields")
            return

        try:
            amount = float(amount)
        except:
            messagebox.showerror("Error", "Amount must be number")
            return

        self.expenses.append({"name": name, "amount": amount})
        self.save_data()
        self.update_table()

        self.name_var.set("")
        self.amount_var.set("")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            return

        index = self.tree.index(selected[0])
        del self.expenses[index]

        self.save_data()
        self.update_table()

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        total = 0
        for item in self.expenses:
            self.tree.insert("", "end", values=(item["name"], item["amount"]))
            total += item["amount"]

        self.total_label.config(text=f"Total: ₹{total:.2f}")

    def save_data(self):
        with open(FILE, "w") as f:
            json.dump(self.expenses, f)

    def load_data(self):
        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                try:
                    self.expenses = json.load(f)
                except:
                    self.expenses = []


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()