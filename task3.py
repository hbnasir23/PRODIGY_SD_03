import tkinter as tk
from tkinter import ttk, messagebox

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if name and phone and email:
        contacts[name] = {'Phone': phone, 'Email': email}
        messagebox.showinfo("Success", "Contact added successfully!")
        clear_entries()
        view_contacts()
        save_contacts()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def view_contacts():
    contact_tree.delete(*contact_tree.get_children())
    for index, (name, contact) in enumerate(contacts.items(), start=1):
        contact_tree.insert("", "end", values=(index, name, contact['Phone'], contact['Email']))

def delete_contact():
    selected_item = contact_tree.selection()
    if selected_item:
        name = contact_tree.item(selected_item, 'values')[1]
        del contacts[name]
        view_contacts()
        save_contacts()
    else:
        messagebox.showerror("Error", "Please select a contact to delete.")

def edit_contact():
    selected_item = contact_tree.selection()
    if selected_item:
        name = contact_tree.item(selected_item, 'values')[1]
        phone = contact_tree.item(selected_item, 'values')[2]
        email = contact_tree.item(selected_item, 'values')[3]
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Contact")

        ttk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="E")
        edit_name_entry = ttk.Entry(edit_window)
        edit_name_entry.insert(tk.END, name)
        edit_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky="E")
        edit_phone_entry = ttk.Entry(edit_window)
        edit_phone_entry.insert(tk.END, phone)
        edit_phone_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="E")
        edit_email_entry = ttk.Entry(edit_window)
        edit_email_entry.insert(tk.END, email)
        edit_email_entry.grid(row=2, column=1, padx=5, pady=5)

        save_button = ttk.Button(edit_window, text="Save Changes",
                                 command=lambda: save_edited_contact(name,
                                                                      edit_name_entry.get(),
                                                                      edit_phone_entry.get(),
                                                                      edit_email_entry.get(),
                                                                      edit_window))
        save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    else:
        messagebox.showerror("Error", "Please select a contact to edit.")

def save_edited_contact(old_name, name, phone, email, edit_window):
    if old_name in contacts:
        del contacts[old_name]
        contacts[name] = {'Phone': phone, 'Email': email}
        view_contacts()
        save_contacts()
        edit_window.destroy()

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

def save_contacts():
    with open("contacts.txt", "w") as file:
        for name, contact in contacts.items():
            file.write(f"{name},{contact['Phone']},{contact['Email']}\n")

def load_contacts():
    try:
        with open("contacts.txt", "r") as file:
            for line in file:
                name, phone, email = line.strip().split(',')
                contacts[name] = {'Phone': phone, 'Email': email}
    except FileNotFoundError:
        pass

contacts = {}

# GUI Setup
root = tk.Tk()
root.title("Contact Manager")
root.geometry("600x400")
root.configure(bg="green")

# Create frame
frame = ttk.Frame(root, padding=10)
frame.pack(fill='both', expand=True)

# Create Treeview
contact_tree = ttk.Treeview(frame, columns=("Index", "Name", "Phone", "Email"), show="headings")
contact_tree.heading("Index", text="Index")
contact_tree.heading("Name", text="Name")
contact_tree.heading("Phone", text="Phone")
contact_tree.heading("Email", text="Email")
contact_tree.pack(fill='both', expand=True)
contact_tree["style"] = "mystyle.Treeview"

# Labels and Entries
label_frame = ttk.LabelFrame(frame, text="Contact Information")
label_frame.pack(fill='both', padx=10, pady=10)

ttk.Label(label_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="E")
name_entry = ttk.Entry(label_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")

ttk.Label(label_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky="E")
phone_entry = ttk.Entry(label_frame)
phone_entry.grid(row=1, column=1, padx=5, pady=5, sticky="W")

ttk.Label(label_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="E")
email_entry = ttk.Entry(label_frame)
email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="W")

# Buttons
add_button = ttk.Button(label_frame, text="Add Contact", command=add_contact)
add_button.grid(row=0, column=2, columnspan=2, padx=5, pady=5, ipadx=20, ipady=5)
add_button_style = ttk.Style()
add_button_style.configure("AddButton.TButton", background="blue")
add_button.config(style="AddButton.TButton")

delete_button = ttk.Button(label_frame, text="Delete Contact", command=delete_contact)
delete_button.grid(row=1, column=2, columnspan=2, padx=5, pady=5, ipadx=20, ipady=5)
delete_button_style = ttk.Style()
delete_button_style.configure("DeleteButton.TButton", background="green")
delete_button.config(style="DeleteButton.TButton")

edit_button = ttk.Button(label_frame, text="Edit Contact", command=edit_contact)
edit_button.grid(row=2, column=2, columnspan=2, padx=5, pady=5, ipadx=20, ipady=5)
edit_button_style = ttk.Style()
edit_button_style.configure("EditButton.TButton", background="yellow")
edit_button.config(style="EditButton.TButton")

# Load existing contacts
load_contacts()
view_contacts()

style = ttk.Style()
style.theme_create("mystyle", parent="alt", settings={
    "Treeview": {"configure": {"background": "light blue", "foreground": "black"}},
    "Treeview.Heading": {"configure": {"background": "teal", "foreground": "white"}},
})
style.theme_use("mystyle")

root.mainloop()
