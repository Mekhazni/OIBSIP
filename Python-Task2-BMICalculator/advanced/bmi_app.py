import tkinter as tk
from tkinter import ttk, messagebox

from bmi_logic import (
    calculate_bmi,
    get_bmi_category,
    get_category_color
)

from database import (
    initialize_database,
    get_users,
    add_user,
    save_bmi_record,
    get_bmi_history
)

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BMIApp:

    def __init__(self, root):

        self.root = root

        self.root.title("BMI Tracker")
        self.root.geometry("600x650")
        self.root.minsize(500, 500)

        # -----------------------------------------------------
        # APPLICATION STATE
        # -----------------------------------------------------

        self.users = []

        # No user is selected when application starts
        self.selected_user_id = None

        self.history_visible = False

        # -----------------------------------------------------
        # CREATE GUI
        # -----------------------------------------------------

        self.create_scrollable_window()
        self.create_widgets()

        # -----------------------------------------------------
        # DATABASE
        # -----------------------------------------------------

        try:

            initialize_database()
            self.load_users()

        except RuntimeError as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # =========================================================
    # SCROLLABLE MAIN WINDOW
    # =========================================================

    def create_scrollable_window(self):

        self.canvas = tk.Canvas(
            self.root,
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.main_scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.main_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=self.main_scrollbar.set
        )

        self.main_frame = ttk.Frame(
            self.canvas
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.main_frame,
            anchor="nw"
        )

        self.main_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_main_frame
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_main_frame(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # =========================================================
    # CREATE MAIN GUI
    # =========================================================

    def create_widgets(self):

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        title = ttk.Label(
            self.main_frame,
            text="BMI TRACKER",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=(25, 5)
        )

        subtitle = ttk.Label(
            self.main_frame,
            text="Calculate and track your Body Mass Index"
        )

        subtitle.pack(
            pady=(0, 20)
        )

        # -----------------------------------------------------
        # USER SECTION
        # -----------------------------------------------------

        user_frame = ttk.LabelFrame(
            self.main_frame,
            text="User"
        )

        user_frame.pack(
            padx=25,
            pady=10,
            fill="x"
        )

        ttk.Label(
            user_frame,
            text="Select user:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=15
        )

        # IMPORTANT:
        # "Select a user..." is a placeholder.
        # It is NOT an actual user.

        self.user_combobox = ttk.Combobox(
            user_frame,
            state="readonly",
            width=22
        )

        self.user_combobox.grid(
            row=0,
            column=1,
            padx=10,
            pady=15
        )

        self.user_combobox.bind(
            "<<ComboboxSelected>>",
            self.on_user_selected
        )

        add_user_button = ttk.Button(
            user_frame,
            text="Add New User",
            command=self.open_add_user_window
        )

        add_user_button.grid(
            row=0,
            column=2,
            padx=10
        )

        # -----------------------------------------------------
        # BMI INPUT SECTION
        # -----------------------------------------------------

        input_frame = ttk.LabelFrame(
            self.main_frame,
            text="BMI Calculator"
        )

        input_frame.pack(
            padx=25,
            pady=10,
            fill="x"
        )

        ttk.Label(
            input_frame,
            text="Weight (kg):"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=15
        )

        self.weight_entry = ttk.Entry(
            input_frame,
            width=20
        )

        self.weight_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=15
        )

        ttk.Label(
            input_frame,
            text="Height (m):"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=15
        )

        self.height_entry = ttk.Entry(
            input_frame,
            width=20
        )

        self.height_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=15
        )

        calculate_button = ttk.Button(
            input_frame,
            text="Calculate BMI",
            command=self.calculate_and_save
        )

        calculate_button.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=20
        )

        # -----------------------------------------------------
        # BMI RESULT
        # -----------------------------------------------------

        self.result_label = tk.Label(
            self.main_frame,
            text="No BMI calculated yet",
            font=("Arial", 18, "bold")
        )

        self.result_label.pack(
            pady=(15, 5)
        )

        self.category_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 16, "bold")
        )

        self.category_label.pack()

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_label = ttk.Label(
            self.main_frame,
            text="Please select a user"
        )

        self.status_label.pack(
            pady=10
        )

        # -----------------------------------------------------
        # HISTORY BUTTON
        # -----------------------------------------------------

        self.history_button = ttk.Button(
            self.main_frame,
            text="View History",
            command=self.toggle_history
        )

        self.history_button.pack(
            pady=10
        )

        # -----------------------------------------------------
        # HISTORY SECTION
        # -----------------------------------------------------

        self.create_history_section()

    # =========================================================
    # HISTORY SECTION
    # =========================================================

    def create_history_section(self):

        self.history_frame = ttk.LabelFrame(
            self.main_frame,
            text="BMI History"
        )

        # -----------------------------------------------------
        # TABLE FRAME
        # -----------------------------------------------------

        table_frame = ttk.Frame(
            self.history_frame
        )

        table_frame.pack(
            padx=10,
            pady=10,
            fill="x"
        )

        # -----------------------------------------------------
        # HISTORY TABLE
        # -----------------------------------------------------

        columns = (
            "date",
            "weight",
            "height",
            "bmi",
            "category"
        )

        self.history_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=6
        )

        self.history_table.heading(
            "date",
            text="Date"
        )

        self.history_table.heading(
            "weight",
            text="Weight"
        )

        self.history_table.heading(
            "height",
            text="Height"
        )

        self.history_table.heading(
            "bmi",
            text="BMI"
        )

        self.history_table.heading(
            "category",
            text="Category"
        )

        self.history_table.column(
            "date",
            width=140,
            anchor="center"
        )

        self.history_table.column(
            "weight",
            width=75,
            anchor="center"
        )

        self.history_table.column(
            "height",
            width=75,
            anchor="center"
        )

        self.history_table.column(
            "bmi",
            width=65,
            anchor="center"
        )

        self.history_table.column(
            "category",
            width=100,
            anchor="center"
        )

        # -----------------------------------------------------
        # TABLE SCROLLBAR
        # -----------------------------------------------------

        table_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.history_table.yview
        )

        self.history_table.configure(
            yscrollcommand=table_scrollbar.set
        )

        self.history_table.pack(
            side="left",
            fill="x",
            expand=True
        )

        table_scrollbar.pack(
            side="right",
            fill="y"
        )

        # -----------------------------------------------------
        # GRAPH BUTTON
        # -----------------------------------------------------

        button_frame = ttk.Frame(
            self.history_frame
        )

        button_frame.pack(
            pady=10
        )

        self.graph_button = ttk.Button(
            button_frame,
            text="View Graph",
            command=self.show_graph
        )

        self.graph_button.pack()

    # =========================================================
    # LOAD USERS
    # =========================================================

    def load_users(self):

        self.users = get_users()

        names = [
            user[1]
            for user in self.users
        ]

        # -----------------------------------------------------
        # IMPORTANT
        #
        # The first item is a placeholder.
        # It is NOT a real user.
        # -----------------------------------------------------

        self.user_combobox["values"] = (
            ["Select a user..."] + names
        )

        # Select placeholder

        self.user_combobox.current(0)

        # No actual user selected

        self.selected_user_id = None

        self.status_label.config(
            text="Please select a user"
        )

    # =========================================================
    # USER SELECTED
    # =========================================================

    def on_user_selected(self, event=None):

        index = self.user_combobox.current()

        # -----------------------------------------------------
        # PLACEHOLDER SELECTED
        # -----------------------------------------------------

        if index == 0:

            self.selected_user_id = None

            self.status_label.config(
                text="Please select a user"
            )

            return

        # -----------------------------------------------------
        # REAL USER SELECTED
        #
        # Subtract 1 because index 0 is the placeholder.
        # -----------------------------------------------------

        user_index = index - 1

        self.selected_user_id = (
            self.users[user_index][0]
        )

        selected_name = (
            self.users[user_index][1]
        )

        self.status_label.config(
            text=f"Selected user: {selected_name}"
        )

        self.result_label.config(
            text="No BMI calculated yet"
        )

        self.category_label.config(
            text=""
        )

        self.weight_entry.delete(
            0,
            tk.END
        )

        self.height_entry.delete(
            0,
            tk.END
        )

        # Hide history when changing users

        self.hide_history()

        # Scroll back to top

        self.canvas.yview_moveto(0)

    # =========================================================
    # ADD NEW USER
    # =========================================================

    def open_add_user_window(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Add New User"
        )

        window.geometry(
            "350x180"
        )

        window.resizable(
            False,
            False
        )

        ttk.Label(
            window,
            text="Enter user name:"
        ).pack(
            pady=15
        )

        name_entry = ttk.Entry(
            window,
            width=30
        )

        name_entry.pack(
            pady=5
        )

        name_entry.focus()

        def save_user():

            name = name_entry.get().strip()

            if not name:

                messagebox.showwarning(
                    "Invalid Name",
                    "Please enter a name.",
                    parent=window
                )

                return

            try:

                add_user(name)

                # Reload users

                self.load_users()

                # Find newly created user

                for index, user in enumerate(self.users):

                    if user[1] == name:

                        # +1 because index 0 is placeholder

                        self.user_combobox.current(
                            index + 1
                        )

                        self.selected_user_id = (
                            user[0]
                        )

                        self.status_label.config(
                            text=f"Selected user: {name}"
                        )

                        break

                window.destroy()

                messagebox.showinfo(
                    "User Added",
                    f"{name} was added successfully."
                )

            except RuntimeError as error:

                messagebox.showerror(
                    "Database Error",
                    str(error),
                    parent=window
                )

        ttk.Button(
            window,
            text="Save User",
            command=save_user
        ).pack(
            pady=15
        )

    # =========================================================
    # CALCULATE BMI
    # =========================================================

    def calculate_and_save(self):

        # -----------------------------------------------------
        # CHECK USER
        # -----------------------------------------------------

        if self.selected_user_id is None:

            messagebox.showwarning(
                "No User Selected",
                "Please select or create a user first."
            )

            return

        # -----------------------------------------------------
        # READ INPUT
        # -----------------------------------------------------

        try:

            weight = float(
                self.weight_entry.get()
            )

            height = float(
                self.height_entry.get()
            )

            # Reject zero and negative values

            if weight <= 0 or height <= 0:

                raise ValueError

            # -------------------------------------------------
            # CALCULATE
            # -------------------------------------------------

            bmi = calculate_bmi(
                weight,
                height
            )

            category = get_bmi_category(
                bmi
            )

            # -------------------------------------------------
            # DISPLAY RESULT
            # -------------------------------------------------

            self.result_label.config(
                text=f"BMI: {bmi:.2f}"
            )

            self.category_label.config(
                text=category,
                fg=get_category_color(category)
            )

            # -------------------------------------------------
            # SAVE TO DATABASE
            # -------------------------------------------------

            try:

                save_bmi_record(
                    self.selected_user_id,
                    weight,
                    height,
                    bmi,
                    category
                )

                self.status_label.config(
                    text="BMI calculated and saved successfully."
                )

                # Refresh history if it is currently visible

                if self.history_visible:

                    self.load_history()

            except RuntimeError as error:

                messagebox.showerror(
                    "Database Error",
                    str(error)
                )

        except ValueError:

            messagebox.showwarning(
                "Invalid Input",
                "Please enter valid positive numbers for weight and height."
            )

    # =========================================================
    # TOGGLE HISTORY
    # =========================================================

    def toggle_history(self):

        # -----------------------------------------------------
        # NO USER SELECTED
        # -----------------------------------------------------

        if self.selected_user_id is None:

            messagebox.showwarning(
                "No User Selected",
                "Please select a user first."
            )

            return

        # -----------------------------------------------------
        # HIDE HISTORY
        # -----------------------------------------------------

        if self.history_visible:

            self.hide_history()

        # -----------------------------------------------------
        # SHOW HISTORY
        # -----------------------------------------------------

        else:

            self.show_history()

    # =========================================================
    # SHOW HISTORY
    # =========================================================

    def show_history(self):

        self.load_history()

        self.history_frame.pack(
            padx=25,
            pady=10,
            fill="x"
        )

        self.history_button.config(
            text="Hide History"
        )

        self.history_visible = True

    # =========================================================
    # HIDE HISTORY
    # =========================================================

    def hide_history(self):

        self.history_frame.pack_forget()

        self.history_button.config(
            text="View History"
        )

        self.history_visible = False

    # =========================================================
    # LOAD HISTORY
    # =========================================================

    def load_history(self):

        # Remove old table rows

        for row in self.history_table.get_children():

            self.history_table.delete(row)

        try:

            history = get_bmi_history(
                self.selected_user_id
            )

        except RuntimeError as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

            return

        # Add records

        for record in history:

            bmi = record[0]
            category = record[1]
            recorded_at = record[2]
            weight = record[3]
            height = record[4]

            self.history_table.insert(
                "",
                "end",
                values=(
                    recorded_at,
                    f"{weight:.2f}",
                    f"{height:.2f}",
                    f"{bmi:.2f}",
                    category
                )
            )

    # =========================================================
    # SHOW GRAPH
    # =========================================================

    def show_graph(self):

        # -----------------------------------------------------
        # CHECK USER
        # -----------------------------------------------------

        if self.selected_user_id is None:

            messagebox.showwarning(
                "No User Selected",
                "Please select a user first."
            )

            return

        # -----------------------------------------------------
        # GET HISTORY
        # -----------------------------------------------------

        try:

            history = get_bmi_history(
                self.selected_user_id
            )

        except RuntimeError as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

            return

        # -----------------------------------------------------
        # NO DATA
        # -----------------------------------------------------

        if not history:

            messagebox.showinfo(
                "No History",
                "This user does not have any BMI records yet."
            )

            return

        user_name = self.user_combobox.get()

        # -----------------------------------------------------
        # CREATE GRAPH WINDOW
        # -----------------------------------------------------

        window = tk.Toplevel(
            self.root
        )

        window.title(
            f"{user_name} - BMI History"
        )

        window.geometry(
            "700x550"
        )

        # -----------------------------------------------------
        # CREATE MATPLOTLIB FIGURE
        # -----------------------------------------------------

        figure = Figure(
            figsize=(7, 4),
            dpi=100
        )

        axis = figure.add_subplot(111)

        dates = [
            record[2]
            for record in history
        ]

        bmi_values = [
            record[0]
            for record in history
        ]

        axis.plot(
            dates,
            bmi_values,
            marker="o"
        )

        axis.set_title(
            f"{user_name}'s BMI Trend"
        )

        axis.set_xlabel(
            "Date"
        )

        axis.set_ylabel(
            "BMI"
        )

        axis.tick_params(
            axis="x",
            rotation=45
        )

        figure.tight_layout()

        # -----------------------------------------------------
        # DISPLAY GRAPH IN TKINTER
        # -----------------------------------------------------

        graph_canvas = FigureCanvasTkAgg(
            figure,
            master=window
        )

        graph_canvas.draw()

        graph_canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )


# =============================================================
# START APPLICATION
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BMIApp(root)

    root.mainloop()
