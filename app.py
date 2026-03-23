
import tkinter as tk
from tkinter import messagebox

# Country rules
country_rules = {
    "🇮🇳 India (+91)": 10,
    "🇺🇸 USA (+1)": 10,
    "🇬🇧 UK (+44)": 11
}

# -------- FUNCTIONS -------- #

def limit_phone_length(*args):
    phone = phone_var.get()
    country = country_var.get()
    max_len = country_rules[country]

    if len(phone) > max_len:
        phone_var.set(phone[:max_len])


def load_contacts():
    contact_list.delete(0, tk.END)
    try:
        with open("contacts.txt", "r", encoding="utf-8") as file:
            for line in file:
                contact_list.insert(tk.END, line.strip())
    except FileNotFoundError:
        pass


def add_contact():
    name = name_entry.get()
    phone = phone_var.get()
    country = country_var.get()

    if name == "" or phone == "":
        messagebox.showwarning("Error", "Please fill all fields")
        return

    if not phone.isdigit():
        messagebox.showwarning("Error", "Phone must contain only numbers")
        return

    required_length = country_rules[country]
    if len(phone) != required_length:
        messagebox.showwarning(
            "Error",
            f"{country} numbers must be {required_length} digits"
        )
        return

    with open("contacts.txt", "a", encoding="utf-8") as file:
        file.write(f"{country} | {name} | {phone}\n")

    messagebox.showinfo("Success", "Contact Saved Successfully!")

    name_entry.delete(0, tk.END)
    phone_var.set("")
    load_contacts()


def delete_contact():
    selected = contact_list.curselection()

    if not selected:
        messagebox.showwarning("Error", "Select a contact to delete")
        return

    contact_to_delete = contact_list.get(selected[0])

    with open("contacts.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open("contacts.txt", "w", encoding="utf-8") as file:
        for line in lines:
            if line.strip() != contact_to_delete:
                file.write(line)

    messagebox.showinfo("Success", "Contact Deleted!")
    load_contacts()


# -------- UI -------- #

root = tk.Tk()
root.title("Contact Manager")
root.geometry("450x500")
root.configure(bg="#121212")

# Title
tk.Label(root, text="Contact Manager", fg="white", bg="#121212",
         font=("Arial", 16, "bold")).pack(pady=10)

# Country
tk.Label(root, text="Country", fg="#cccccc", bg="#121212").pack()
country_var = tk.StringVar()
country_var.set("🇮🇳 India (+91)")

country_menu = tk.OptionMenu(root, country_var, *country_rules.keys())
country_menu.config(bg="#1e1e1e", fg="white", activebackground="#333333")
country_menu.pack(pady=5)

# Name
tk.Label(root, text="Name", fg="#cccccc", bg="#121212").pack()
name_entry = tk.Entry(root, width=30, bg="#1e1e1e", fg="white", insertbackground="white")
name_entry.pack(pady=5)

# Phone
tk.Label(root, text="Phone", fg="#cccccc", bg="#121212").pack()

phone_var = tk.StringVar()
phone_var.trace("w", limit_phone_length)

phone_entry = tk.Entry(root, textvariable=phone_var, width=30,
                       bg="#1e1e1e", fg="white", insertbackground="white")
phone_entry.pack(pady=5)

# Hover effect
def on_enter(e):
    e.widget['background'] = '#00c853'

def on_leave(e):
    e.widget['background'] = '#00a843'

# Buttons
add_btn = tk.Button(root, text="Add Contact",
                    bg="#00a843", fg="white",
                    font=("Arial", 11, "bold"),
                    width=20, command=add_contact,
                    relief="flat")
add_btn.pack(pady=10)

del_btn = tk.Button(root, text="Delete Selected",
                    bg="#00a843", fg="white",
                    font=("Arial", 11, "bold"),
                    width=20, command=delete_contact,
                    relief="flat")
del_btn.pack(pady=5)

# Hover binding
for btn in [add_btn, del_btn]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Contact List
tk.Label(root, text="Saved Contacts", fg="#cccccc", bg="#121212").pack(pady=10)

frame = tk.Frame(root)
frame.pack()

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

contact_list = tk.Listbox(frame, width=50, height=10,
                         bg="#1e1e1e", fg="white",
                         yscrollcommand=scrollbar.set)

contact_list.pack()
scrollbar.config(command=contact_list.yview)

# Load contacts
load_contacts()

root.mainloop()