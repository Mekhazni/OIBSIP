import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

from password_generator import (
    generate_password,
    calculate_password_strength
)


root = tk.Tk()

root.title("Password Generator")
root.geometry("500x650")
root.resizable(False, False)


title_label = ttk.Label(
    root,
    text="Password Generator",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=20)


length_label = ttk.Label(
    root,
    text="Password Length:"
)

length_label.pack()


length_spinbox = ttk.Spinbox(
    root,
    from_=8,
    to=64,
    width=10
)

length_spinbox.set(16)
length_spinbox.pack(pady=5)


types_label = ttk.Label(
    root,
    text="Character Types",
    font=("Arial", 12, "bold")
)

types_label.pack(pady=(20, 10))


uppercase_var = tk.BooleanVar(value=False)
lowercase_var = tk.BooleanVar(value=False)
numbers_var = tk.BooleanVar(value=False)
symbols_var = tk.BooleanVar(value=False)


uppercase_checkbox = ttk.Checkbutton(
    root,
    text="Uppercase letters",
    variable=uppercase_var
)

uppercase_checkbox.pack(anchor="w", padx=150)


lowercase_checkbox = ttk.Checkbutton(
    root,
    text="Lowercase letters",
    variable=lowercase_var
)

lowercase_checkbox.pack(anchor="w", padx=150)


numbers_checkbox = ttk.Checkbutton(
    root,
    text="Numbers",
    variable=numbers_var
)

numbers_checkbox.pack(anchor="w", padx=150)


symbols_checkbox = ttk.Checkbutton(
    root,
    text="Symbols",
    variable=symbols_var
)

symbols_checkbox.pack(anchor="w", padx=150)


exclude_ambiguous_var = tk.BooleanVar(value=False)

exclude_ambiguous_checkbox = ttk.Checkbutton(
    root,
    text="Exclude ambiguous characters (0, O, l, 1, I)",
    variable=exclude_ambiguous_var
)

exclude_ambiguous_checkbox.pack(pady=20)




password_var = tk.StringVar()

strength_var = tk.StringVar()

password_history = []

password_label = ttk.Label(
    root,
    textvariable=password_var,
    font=("Arial", 14)
)

password_label.pack(pady=10)

strength_label = ttk.Label(
    root,
    textvariable=strength_var,
    font=("Arial", 12, "bold")
)

strength_label.pack(pady=5)

def update_history(password):
    password_history.insert(0, password)

    if len(password_history) > 5:
        password_history.pop()

    history_listbox.delete(0, tk.END)

    for item in password_history:
        history_listbox.insert(tk.END, item)

def generate_password_from_gui():
    try:
        # Get the password length
        length = int(length_spinbox.get())

        # Get the selected character types
        use_uppercase = uppercase_var.get()
        use_lowercase = lowercase_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()

        # Get the ambiguous-character setting
        exclude_ambiguous = exclude_ambiguous_var.get()

        # Generate the password
        password = generate_password(
            length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_numbers=use_numbers,
            use_symbols=use_symbols,
            exclude_ambiguous=exclude_ambiguous
        )

        # Display the password
        password_var.set(password)

        # Automatically copy the password
        pyperclip.copy(password)

       # Add password to generation history
        update_history(password)

        strength = calculate_password_strength(
            length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_numbers=use_numbers,
            use_symbols=use_symbols
        )

        # Display password strength
        strength_var.set(f"Strength: {strength}")

    except ValueError as error:
        messagebox.showerror("Invalid Input", str(error))


def copy_password():
    password = password_var.get()

    if password:
        pyperclip.copy(password)
        messagebox.showinfo(
            "Copied",
            "Password copied to clipboard."
        )
    else:
        messagebox.showwarning(
            "No Password",
            "Please generate a password first."
        )


copy_button = ttk.Button(
    root,
    text="Copy to Clipboard",
    command=copy_password
)

copy_button.pack(pady=10)



generate_button = ttk.Button(
    root,
    text="Generate Password",
    command=generate_password_from_gui
)

generate_button.pack(pady=15)

history_label = ttk.Label(
    root,
    text="Generation History"
)

history_label.pack(pady=(15, 5))


history_listbox = tk.Listbox(
    root,
    width=35,
    height=5
)

history_listbox.pack(pady=5)


root.mainloop()