import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

DATA_FILE = "library_data.json"
USERS = {"admin": "admin123", "student": "student123"}
FINE_PER_DAY = 5
FREE_DAYS = 7

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"books": {}, "issued": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ---------------- LOGIN ----------------
def login():
    user = user_entry.get()
    pwd = pass_entry.get()
    if user in USERS and USERS[user] == pwd:
        login_frame.pack_forget()
        main_menu(user)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

# ---------------- MAIN MENU ----------------
def main_menu(user):
    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text=f"Welcome {user}", font=("Arial", 16)).pack(pady=10)

    if user == "admin":
        tk.Button(frame, text="Add Book", width=25, command=add_book_ui).pack(pady=3)

    tk.Button(frame, text="View Books", width=25, command=view_books_ui).pack(pady=3)
    tk.Button(frame, text="Search Book", width=25, command=search_book_ui).pack(pady=3)
    tk.Button(frame, text="Issue Book", width=25, command=issue_book_ui).pack(pady=3)
    tk.Button(frame, text="Return Book", width=25, command=return_book_ui).pack(pady=3)
    tk.Button(frame, text="Logout", width=25, command=root.quit).pack(pady=3)

# ---------------- UI FUNCTIONS ----------------
def add_book_ui():
    win = tk.Toplevel(root)
    win.title("Add Book")

    tk.Label(win, text="Book ID").pack()
    bid = tk.Entry(win); bid.pack()
    tk.Label(win, text="Title").pack()
    title = tk.Entry(win); title.pack()
    tk.Label(win, text="Author").pack()
    author = tk.Entry(win); author.pack()

    def save():
        data["books"][bid.get()] = {"title": title.get(), "author": author.get()}
        save_data(data)
        messagebox.showinfo("Success", "Book added")
        win.destroy()

    tk.Button(win, text="Save", command=save).pack(pady=5)

def view_books_ui():
    win = tk.Toplevel(root)
    win.title("Available Books")
    if not data["books"]:
        tk.Label(win, text="No books available").pack()
    for bid, b in data["books"].items():
        tk.Label(win, text=f"{bid} - {b['title']} by {b['author']}").pack(anchor="w")

def search_book_ui():
    win = tk.Toplevel(root)
    win.title("Search Book")

    tk.Label(win, text="Enter Book ID or Title").pack()
    query = tk.Entry(win); query.pack()

    result_label = tk.Label(win, text="")
    result_label.pack(pady=5)

    def search():
        q = query.get().lower()
        for bid, b in data["books"].items():
            if q == bid.lower() or q in b["title"].lower():
                result_label.config(text=f"Found: {bid} - {b['title']} by {b['author']}")
                return
        result_label.config(text="Book not found")

    tk.Button(win, text="Search", command=search).pack(pady=5)

def issue_book_ui():
    win = tk.Toplevel(root)
    win.title("Issue Book")

    tk.Label(win, text="Book ID").pack()
    bid = tk.Entry(win); bid.pack()
    tk.Label(win, text="Student Name").pack()
    student = tk.Entry(win); student.pack()

    def issue():
        if bid.get() in data["books"]:
            data["issued"][bid.get()] = {
                "student": student.get(),
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            del data["books"][bid.get()]
            save_data(data)
            messagebox.showinfo("Issued", "Book issued successfully")
            win.destroy()
        else:
            messagebox.showerror("Error", "Book not available")

    tk.Button(win, text="Issue", command=issue).pack(pady=5)

def return_book_ui():
    win = tk.Toplevel(root)
    win.title("Return Book")

    tk.Label(win, text="Book ID").pack()
    bid = tk.Entry(win); bid.pack()
    tk.Label(win, text="Title").pack()
    title = tk.Entry(win); title.pack()
    tk.Label(win, text="Author").pack()
    author = tk.Entry(win); author.pack()

    def ret():
        if bid.get() in data["issued"]:
            issue_date = datetime.strptime(data["issued"][bid.get()]["date"], "%Y-%m-%d")
            days = (datetime.now() - issue_date).days
            fine = max(0, days - FREE_DAYS) * FINE_PER_DAY

            data["books"][bid.get()] = {"title": title.get(), "author": author.get()}
            del data["issued"][bid.get()]
            save_data(data)

            messagebox.showinfo("Returned", f"Book returned.\nFine: Rs {fine}")
            win.destroy()
        else:
            messagebox.showerror("Error", "Book not found")

    tk.Button(win, text="Return", command=ret).pack(pady=5)

# ---------------- MAIN ----------------
root = tk.Tk()
root.title("Library Management System")
root.geometry("320x350")

login_frame = tk.Frame(root)
login_frame.pack(pady=40)

tk.Label(login_frame, text="Username").pack()
user_entry = tk.Entry(login_frame); user_entry.pack()
tk.Label(login_frame, text="Password").pack()
pass_entry = tk.Entry(login_frame, show="*"); pass_entry.pack()
tk.Button(login_frame, text="Login", command=login).pack(pady=10)

root.mainloop()