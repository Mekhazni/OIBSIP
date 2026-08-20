# BMI Calculator

A BMI Calculator developed as part of the Oasis Infobyte Python Programming Internship.

## Project Overview

This project is a Python-based BMI tracking application that allows users to calculate their Body Mass Index (BMI), classify the result into standard BMI categories, and keep track of their BMI measurements.

The project was developed in two stages:

- Beginner: Command-line BMI calculator
- Advanced: Graphical BMI tracking application with user management, history storage, and BMI trend visualization

## Features

### Beginner Version

- Enter weight in kilograms
- Enter height in meters
- Calculate BMI
- Classify BMI into:
  - Underweight
  - Normal
  - Overweight
  - Obese
- Display BMI rounded to two decimal places
- Validate user input

### Advanced Version

- Graphical user interface built with Tkinter
- Create and select users
- Unique usernames
- Calculate BMI for the selected user
- Save BMI records using SQLite
- View BMI history in a table
- View BMI trend using a graph
- Input validation and error handling
- Database error handling

## Technologies Used

- Python
- Tkinter
- SQLite
- Matplotlib

## Project Structure

Python-Task2-BMICalculator/
├── beginner/
│   └── bmi_calculator.py
├── advanced/
│   ├── bmi_app.py
│   ├── bmi_logic.py
│   └── database.py
└── README.md

## How to Run

### Beginner Version

1. Make sure Python is installed.
2. Open a terminal in the project directory.
3. Run:

python beginner/bmi_calculator.py

### Advanced Version

1. Make sure Python is installed.
2. Install Matplotlib:

pip install matplotlib

3. Open a terminal in the project directory.
4. Run:

python advanced/bmi_app.py

## Requirements

- Python 3.12 or later
- Tkinter
- SQLite3
- Matplotlib

## BMI Formula

BMI = weight / (height²)

### BMI Categories

| BMI | Category |
|---|---|
| < 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25 – 29.9 | Overweight |
| ≥ 30 | Obese |

## Internship

Program: Oasis Infobyte Python Programming Internship

Track: Python Programming

Task: Task 2 — BMI Calculator
