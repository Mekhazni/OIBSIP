# Password Generator

A secure password generator built with Python and Tkinter as part of the Oasis Infobyte Internship Program.

The application generates random passwords based on user-defined criteria and provides additional security and usability features such as password strength evaluation, ambiguous-character exclusion, clipboard integration, and temporary generation history.

## Features

- Generate passwords with a user-defined length from 8 to 64 characters.
- Select the character types to include:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Symbols
- Enforce a minimum password length of 8 characters.
- Require at least two character types to be selected.
- Guarantee at least one character from every selected character type.
- Use Python's secrets module for cryptographically secure password generation.
- Securely shuffle generated password characters.
- Display password strength as Weak, Medium, or Strong.
- Exclude ambiguous characters such as 0, O, l, 1, and I.
- Automatically copy the generated password to the system clipboard.
- Provide a "Copy to Clipboard" button.
- Display the last five generated passwords during the current session.
- Password history is stored only in memory and is not persisted to a file.

## Technologies Used

- Python 3
- Tkinter
- secrets
- string
- pyperclip

## Project Structure

Python-Task3-PasswordGenerator/
├── gui.py
├── password_generator.py
├── README.md
└── screenshots/
    └── password-generator.png

## How It Works

The project is divided into two Python files to keep the password-generation logic separate from the graphical user interface.

### password_generator.py

This file contains the core password-generation logic.

The generate_password() function:

1. Validates the requested password length.
2. Checks that at least two character types have been selected.
3. Builds character sets based on the user's selections.
4. Removes ambiguous characters when the option is enabled.
5. Guarantees at least one character from each selected character type.
6. Combines the selected character sets into a single character pool.
7. Uses the secrets module to securely select random characters.
8. Securely shuffles the generated password.
9. Returns the final password.

The file also contains the calculate_password_strength() function, which evaluates password strength based on password length and character diversity.

### gui.py

This file contains the Tkinter graphical user interface.

The GUI allows the user to:

- Select the password length using a Spinbox.
- Select the desired character types using checkboxes.
- Enable or disable ambiguous-character exclusion.
- Generate a password.
- View the generated password.
- View the password strength.
- Copy the password to the clipboard.
- View the last five generated passwords during the current session.

The GUI also handles invalid input by displaying appropriate error messages.

## Password Security

The application uses Python's secrets module instead of the standard random module for password generation.

The secrets module is designed for generating cryptographically strong random values suitable for security-sensitive applications such as passwords and authentication tokens.

The generator also guarantees that at least one character from every selected character type is included in the final password.

## Ambiguous Characters

The application provides an option to exclude characters that can be visually confused with one another.

When enabled, the generator excludes:

0
O
l
1
I

This can make passwords easier to distinguish when they need to be read or manually entered.

## Password Strength

Password strength is evaluated using two factors:

- Password length
- Character diversity

The application classifies passwords as:

- Weak
- Medium
- Strong

The strength indicator is intended as a simple project-level assessment rather than a comprehensive password security estimator.

## Clipboard Integration

The application uses pyperclip to provide clipboard functionality.

When a password is generated, it is automatically copied to the clipboard. The application also provides a dedicated "Copy to Clipboard" button for copying the currently displayed password again.

## Generation History

The application keeps track of the five most recently generated passwords during the current program session.

The history:

- Displays the newest password first.
- Keeps a maximum of five passwords.
- Removes the oldest password when a sixth password is generated.
- Is stored only in memory.
- Is not written to a file or database.

## Screenshot

![Password Generator](screenshots/password-generator.png)

## Installation

Clone or download the repository and navigate to the project directory.

Create and activate a virtual environment if needed:

python3 -m venv .venv

source .venv/bin/activate

Install the required dependency:

pip install pyperclip

## Running the Application

Run the GUI with:

python gui.py

The Password Generator window will open and allow you to configure and generate passwords.

## References

- Python secrets documentation: https://docs.python.org/3/library/secrets.html
- Python string documentation: https://docs.python.org/3/library/string.html
- Python Tkinter documentation: https://docs.python.org/3/library/tkinter.html
- Pyperclip documentation: https://pypi.org/project/pyperclip/

## Internship Task

Program: Oasis Infobyte Internship Program

Task: Phase 2 — Task 3: Password Generator

Tier: Advanced

This project was developed as part of the Oasis Infobyte internship requirements.
