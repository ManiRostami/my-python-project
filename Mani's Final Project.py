import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import string


class PersonAuthenticator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mani's Final Project")
        self.setup_vars()
        self.setup_ui()
        self.setup_database()

    def setup_vars(self):
        self.landline_input = False
        self.phone_input = False
        self.email_input = False
        self.elements_list = [[None for _ in range(4)] for _ in range(16)]
        self.connection_var_list = [tk.IntVar() for _ in range(3)]
        self.gender_var = tk.IntVar(value=2)
        self.city_town_dict = {
            "Tehran": ["Tehran", "Qods", "Shariyar", "Eslamshahr", "Malard"],
            "Alborz": ["Karaj", "Savojbolagh", "NazarAbad", "Taleghan"],
            "Markazi": ["Arak", "Delijan", "Mahalat", "Saveh", "Tafresh"]
        }

    def setup_ui(self):
        labels = ["ID:", "First Name:", "Last Name:", "Age:", "Height:", "Weight:", "BMI:", "Gender:", "Soldier Status:", "City:", "Town:", "Connections:", "landline Number:", "phone Number:", "Email Address:", "Authenticate"]
        self.create_labels(labels)
        self.create_entries()
        self.create_comboboxes()
        self.create_radiobuttons()
        self.create_checkbuttons()
        self.create_buttons()
        self.layout_widgets()

    def create_labels(self, labels):
        for i, text in enumerate(labels[:-1]):
            self.elements_list[i][0] = tk.Label(self, text=text, font=("Calibri", 20))

    def create_entries(self):
        for i in range(15):
            self.elements_list[i][1] = tk.Entry(self, font=("Calibri", 20, "bold"))
            if i == 6 or i >= 12:
                self.elements_list[i][1].config(state="disabled")

    def create_comboboxes(self):
        self.elements_list[8][1] = ttk.Combobox(self, values=["پایان خدمت", "کفالت", "معافیت موقت", "دانش آموز کلاس دوازدهم"], font=("Calibri", 12), state="disabled")
        self.elements_list[9][1] = ttk.Combobox(self, values=list(self.city_town_dict.keys()), font=("Calibri", 12))
        self.elements_list[9][1].bind("<<ComboboxSelected>>", self.update_towns)
        self.elements_list[10][1] = ttk.Combobox(self, font=("Calibri", 12))

    def create_radiobuttons(self):
        genders = ["Male", "Female","Other"]
        for i, gender in enumerate(genders):
            self.elements_list[7][1 + i] = tk.Radiobutton(self, text=gender, variable=self.gender_var, value=i, command=self.update_soldier_status)

    def create_checkbuttons(self):
        connection_types = ["landline", "phone", "Email"]
        for i, text in enumerate(connection_types):
            self.elements_list[11][i + 1] = tk.Checkbutton(self, text=text, variable=self.connection_var_list[i], offvalue=0, onvalue=1, command=self.update_connections_entry_state)

    def create_buttons(self):
        button_texts = ["Authenticate", "Save", "Clear"]
        button_cmds = [self.authenticator, self.save, self.clear]
        for i, (btn_text, cmd) in enumerate(zip(button_texts, button_cmds)):
            self.elements_list[-1][i] = tk.Button(self, text=btn_text, font=("Calibri", 20), command=cmd)
            if i == 1:
                self.elements_list[-1][i].config(state="disabled")

    def layout_widgets(self):
        for i in range(len(self.elements_list) - 1):
            self.elements_list[i][0].grid(row=i, column=0, sticky="w")
        for i in range(3):
            self.elements_list[-1][i].grid(row=16, column=i, sticky="nsew")
        for i in range(15):
            if not (6 < i < 12):
                self.elements_list[i][1].grid(row=i, column=1, columnspan=3)
        self.elements_list[8][1].grid(row=8, column=1, columnspan=3)
        self.elements_list[9][1].grid(row=9, column=1, columnspan=3)
        self.elements_list[10][1].grid(row=10, column=1, columnspan=3)
        for i in range(3):
            self.elements_list[7][1 + i].grid(row=7, column=1 + i, columnspan=3, sticky="w")
        for i in range(3):
            self.elements_list[11][i + 1].grid(row=11, column=i + 1)

    def setup_database(self):
        self.conn = sqlite3.connect("person_authenticator.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                age INTEGER,
                height REAL,
                weight REAL,
                bmi REAL,
                gender TEXT,
                soldier_status TEXT,
                city TEXT,
                town TEXT,
                landline_number TEXT,
                phone_number TEXT,
                email_address TEXT
            )
        ''')
        self.conn.commit()

    def update_soldier_status(self):
        self.elements_list[8][1].config(state="normal" if self.gender_var.get() == 0 else "disabled")

    def authenticator(self):
        validators = {
            0: self.validate_id,
            1: lambda: self.validate_text(1, "First Name", min_length=3),
            2: lambda: self.validate_text(2, "Last Name", min_length=3),
            3: lambda: self.validate_number(3, "Age", int, 1, 120),
            4: lambda: self.validate_number(4, "Height", float, 0.4, 2.5),
            5: lambda: self.validate_number(5, "Weight", float, 1.0, 250.0),
            6: self.calculate_bmi,
            12: lambda: self.validate_landline(12, "landline number") if self.landline_input else None,
            13: lambda: self.validate_landline(13, "phone number") if self.phone_input else None,
            14: self.validate_email if self.email_input else None,
        }
        self.errors = []
        for i, validator in validators.items():
            if validator:
                validator()
        self.display_results()

    def validate_id(self):
        id_ = self.elements_list[0][1].get()
        if len(id_) != 10 or not id_.isdigit():
            self.errors.append("ID: You must enter 10 numeric characters.")

    def validate_text(self, index, field, min_length):
        text = "".join(self.elements_list[index][1].get().split())
        if not text.isalpha() or len(text) <= min_length:
            self.errors.append(f"{field}: Should be alphabetic and more than {min_length} letters.")

    def validate_number(self, index, field, num_type, min_val, max_val):
        try:
            value = num_type(self.elements_list[index][1].get())
            if not min_val <= value <= max_val:
                raise ValueError(f"Enter a valid number between {min_val} and {max_val}.")
        except ValueError as e:
            self.errors.append(f"{field}: Enter a valid number between {min_val} and {max_val}.")

    def calculate_bmi(self):
        try:
            self.elements_list[6][1].config(state="normal")
            height = float(self.elements_list[4][1].get())
            weight = float(self.elements_list[5][1].get())
            bmi_value = weight / (height ** 2)
            self.elements_list[6][1].delete(0, tk.END)
            self.elements_list[6][1].insert(0, f"{bmi_value:.2f}")
            self.elements_list[6][1].config(state="readonly")
        except:
            self.elements_list[6][1].config(state="readonly")
            

    def validate_landline(self, index, field):
        landline = self.elements_list[index][1].get()
        if not landline.isdigit() or len(landline) != 11 or landline[0] != '0':
            self.errors.append(f"{field}: Must be 11 digits and start with 0.")

    def validate_email(self):
        email = self.elements_list[14][1].get()
        valid_chars = string.ascii_letters + string.digits + "@_."
        if len(email) < 5 or not set(email).issubset(set(valid_chars)):
            self.errors.append("Email: Please enter a valid email address.")

    def display_results(self):
        if not self.errors:
            messagebox.showinfo("Validation", "All information is validated.")
            self.elements_list[-1][1].config(state="normal")
        else:
            numbered_errors = "\n".join(f"{idx + 1}. {error}" for idx, error in enumerate(self.errors))
            messagebox.showwarning("Validation Errors", numbered_errors)


    def update_connections_entry_state(self):
        self.landline_input = self.connection_var_list[0].get()
        self.phone_input = self.connection_var_list[1].get()
        self.email_input = self.connection_var_list[2].get()

        self.elements_list[12][1].config(state="normal" if self.landline_input else "disabled")
        self.elements_list[13][1].config(state="normal" if self.phone_input else "disabled")
        self.elements_list[14][1].config(state="normal" if self.email_input else "disabled")

    def update_towns(self, event=None):
        selected_city = self.elements_list[9][1].get()
        towns = self.city_town_dict.get(selected_city, [])
        self.elements_list[10][1].config(values=towns)
        if towns:
            self.elements_list[10][1].set(towns[0])

    def save(self):
        try:
            data = {
                "id": self.elements_list[0][1].get(),
                "first_name": self.elements_list[1][1].get(),
                "last_name": self.elements_list[2][1].get(),
                "age": int(self.elements_list[3][1].get()),
                "height": float(self.elements_list[4][1].get()),
                "weight": float(self.elements_list[5][1].get()),
                "bmi": float(self.elements_list[6][1].get()),
                "gender": ["Other", "Male", "Female"][self.gender_var.get()],
                "soldier_status": self.elements_list[8][1].get() if self.gender_var.get() == 1 else "",
                "city": self.elements_list[9][1].get(),
                "town": self.elements_list[10][1].get(),
                "landline_number": self.elements_list[12][1].get() if self.landline_input else "",
                "phone_number": self.elements_list[13][1].get() if self.phone_input else "",
                "email_address": self.elements_list[14][1].get() if self.email_input else ""
            }
            self.cursor.execute('''
                INSERT INTO persons (id, first_name, last_name, age, height, weight, bmi, gender, soldier_status, city, town, landline_number, phone_number, email_address)
                VALUES (:id, :first_name, :last_name, :age, :height, :weight, :bmi, :gender, :soldier_status, :city, :town, :landline_number, :phone_number, :email_address)
            ''', data)
            self.conn.commit()
            messagebox.showinfo("Success", "Data saved successfully!")
            self.clear()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "A person with this ID already exists.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {e}")

    def clear(self):
        for row in self.elements_list:
            if row[1] and hasattr(row[1], 'delete'):
                row[1].delete(0, tk.END)
        self.elements_list[6][1].config(state="normal")
        self.elements_list[6][1].delete(0, tk.END)
        self.elements_list[6][1].config(state="readonly")


if __name__ == "__main__":
    app = PersonAuthenticator()
    app.mainloop()
