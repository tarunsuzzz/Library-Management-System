import tkinter as tk
from tkinter import messagebox
import json, os
from datetime import datetime

DATA_FILE = "library_data.json"
USERS = {"admin": "admin123", "student": "student123"}
FINE_PER_DAY = 5
FREE_DAYS = 7

BG_COLOR = "#f4f6fb"
BTN_COLOR = "#4a6cf7"
BTN_TEXT = "white"
FONT_MAIN = ("Segoe UI", 11)
FONT_TITLE = ("Segoe UI", 16, "bold")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"books": {}, "issued": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ---------- AUTH ----------
def login():
    u, p = user_entry.get(), pass_entry.get()
    if u in USERS and USERS[u] == p:
        login_frame.pack_forget()
        main_menu(u)
    else:
        messagebox.showerror("Error", "Invalid credentials")

def logout(frame):
    frame.destroy()
    login_frame.pack(pady=60)

# ---------- UI HELPERS ----------
def styled_button(parent, text, cmd):
    tk.Button(parent, text=text, width=22, bg=BTN_COLOR, fg=BTN_TEXT,
              font=FONT_MAIN, relief="flat", command=cmd).pack(pady=4)

def form_window(title, fields, callback):
    win = tk.Toplevel(root, bg=BG_COLOR)
    win.title(title)
    entries = []

    for f in fields:
        tk.Label(win, text=f, bg=BG_COLOR, font=FONT_MAIN).pack(pady=3)
        e = tk.Entry(win, font=FONT_MAIN)
        e.pack(pady=2)
        entries.append(e)

    def submit():
        values = [e.get() for e in entries]
        callback(values, win)

    styled_button(win, "Submit", submit)

def list_window(title, items):
    win = tk.Toplevel(root, bg=BG_COLOR)
    win.title(title)
    for item in items:
        tk.Label(win, text=item, bg=BG_COLOR, font=FONT_MAIN).pack(anchor="w", padx=10, pady=2)

# ---------- CORE FEATURES ----------
def main_menu(user):
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(pady=20)

    tk.Label(frame, text=f"Welcome {user}", font=FONT_TITLE, bg=BG_COLOR).pack(pady=10)

    if user == "admin":
        styled_button(frame, "Add Book", add_book_ui)

    styled_button(frame, "View Books", view_books_ui)
    styled_button(frame, "Search Book", search_book_ui)
    styled_button(frame, "Issue Book", issue_book_ui)
    styled_button(frame, "Return Book", return_book_ui)
    styled_button(frame, "Logout", lambda: logout(frame))

def add_book_ui():
    form_window("Add Book", ["Book ID", "Title", "Author"], save_add_book)

def save_add_book(values, win):
    bid, title, author = values
    data["books"][bid] = {"title": title, "author": author}
    save_data(data)
    messagebox.showinfo("Success", "Book added")
    win.destroy()

def view_books_ui():
    items = [f"{bid} - {b['title']} by {b['author']}" for bid, b in data["books"].items()]
    list_window("Available Books", items)

def search_book_ui():
    def do_search(val, win):
        q = val[0].strip().lower()
        for bid, b in data["books"].items():
            if q == bid.lower() or q in b["title"].lower():
                messagebox.showinfo("Found", f"{bid} - {b['title']} by {b['author']}")
                return
        messagebox.showerror("Not Found", "Book not found")
    form_window("Search Book", ["Book ID or Title"], do_search)

def issue_book_ui():
    form_window("Issue Book", ["Book ID", "Student Name"], save_issue)

def save_issue(values, win):
    bid, student = values
    if bid in data["books"]:
        data["issued"][bid] = {"student": student, "date": datetime.now().strftime("%Y-%m-%d")}
        del data["books"][bid]
        save_data(data)
        messagebox.showinfo("Issued", "Book issued")
        win.destroy()
    else:
        messagebox.showerror("Error", "Book not available")

def return_book_ui():
    form_window("Return Book", ["Book ID", "Title", "Author"], save_return)

def save_return(values, win):
    bid, title, author = values
    if bid in data["issued"]:
        issue_date = datetime.strptime(data["issued"][bid]["date"], "%Y-%m-%d")
        fine = max(0, (datetime.now() - issue_date).days - FREE_DAYS) * FINE_PER_DAY
        data["books"][bid] = {"title": title, "author": author}
        del data["issued"][bid]
        save_data(data)
        messagebox.showinfo("Returned", f"Book returned.\nFine: Rs {fine}")
        win.destroy()
    else:
        messagebox.showerror("Error", "Invalid book ID")

# ---------- MAIN ----------
root = tk.Tk()
root.title("Library Management System")
root.geometry("360x420")
root.configure(bg=BG_COLOR)

login_frame = tk.Frame(root, bg=BG_COLOR)
login_frame.pack(pady=60)

tk.Label(login_frame, text="Username", bg=BG_COLOR, font=FONT_MAIN).pack()
user_entry = tk.Entry(login_frame, font=FONT_MAIN)
user_entry.pack(pady=4)

tk.Label(login_frame, text="Password", bg=BG_COLOR, font=FONT_MAIN).pack()
pass_entry = tk.Entry(login_frame, show="*", font=FONT_MAIN)
pass_entry.pack(pady=4)

styled_button(login_frame, "Login", login)

root.mainloop()