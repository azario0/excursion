import customtkinter as ctk
import csv
from datetime import datetime
from tkcalendar import DateEntry
import os

class ExcursionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Excursion Management")
        self.geometry("800x600")

        # Ensure CSV files exist
        self.create_csv_files()

        # Create tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_add_excursion = self.tabview.add("Add Excursion")
        self.tab_add_participant = self.tabview.add("Add Participant")
        self.tab_view_excursion = self.tabview.add("View Excursion")
        self.tab_search_participants = self.tabview.add("Search Participants")

        self.setup_add_excursion_tab()
        self.setup_add_participant_tab()
        self.setup_view_excursion_tab()
        self.setup_search_participants_tab()

    def create_csv_files(self):
        files = ['excursions.csv', 'participants.csv']
        for file in files:
            if not os.path.exists(file):
                with open(file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    if file == 'excursions.csv':
                        writer.writerow(['Name', 'Date'])
                    else:
                        writer.writerow(['Name', 'Surname', 'Phone', 'Excursion'])

    def setup_add_excursion_tab(self):
        frame = ctk.CTkFrame(self.tab_add_excursion)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Excursion Name:").pack(pady=5)
        self.excursion_name_entry = ctk.CTkEntry(frame)
        self.excursion_name_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Excursion Date:").pack(pady=5)
        self.excursion_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.excursion_date_entry.pack(pady=5)

        ctk.CTkButton(frame, text="Save Excursion", command=self.save_excursion).pack(pady=20)

        # New dropdown for all excursions
        ctk.CTkLabel(frame, text="All Excursions:").pack(pady=5)
        self.all_excursions_dropdown = ctk.CTkComboBox(frame, values=self.get_all_excursions())
        self.all_excursions_dropdown.pack(pady=5)
        ctk.CTkButton(frame, text="Refresh Excursions", command=self.refresh_excursions).pack(pady=5)

    def setup_add_participant_tab(self):
        frame = ctk.CTkFrame(self.tab_add_participant)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Name:").pack(pady=5)
        self.participant_name_entry = ctk.CTkEntry(frame)
        self.participant_name_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Surname:").pack(pady=5)
        self.participant_surname_entry = ctk.CTkEntry(frame)
        self.participant_surname_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Phone Number:").pack(pady=5)
        self.participant_phone_entry = ctk.CTkEntry(frame)
        self.participant_phone_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Select Excursion:").pack(pady=5)
        self.excursion_combobox = ctk.CTkComboBox(frame, values=self.get_excursion_names())
        self.excursion_combobox.pack(pady=5)

        ctk.CTkButton(frame, text="Save Participant", command=self.save_participant).pack(pady=20)

    def setup_view_excursion_tab(self):
        frame = ctk.CTkFrame(self.tab_view_excursion)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Search Excursion:").pack(pady=5)
        self.search_excursion_entry = ctk.CTkEntry(frame)
        self.search_excursion_entry.pack(pady=5)

        ctk.CTkButton(frame, text="Search", command=self.search_excursion).pack(pady=5)

        self.excursion_listbox = ctk.CTkTextbox(frame, height=200, state="disabled")
        self.excursion_listbox.pack(pady=10, fill="both", expand=True)

    def setup_search_participants_tab(self):
        frame = ctk.CTkFrame(self.tab_search_participants)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Search by Name/Surname:").pack(pady=5)
        self.search_name_entry = ctk.CTkEntry(frame)
        self.search_name_entry.pack(pady=5)
        ctk.CTkButton(frame, text="Search by Name", command=self.search_participants_by_name).pack(pady=5)

        ctk.CTkLabel(frame, text="Search by Date:").pack(pady=5)
        self.search_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.search_date_entry.pack(pady=5)
        ctk.CTkButton(frame, text="Search by Date", command=self.search_participants_by_date).pack(pady=5)

        self.participants_listbox = ctk.CTkTextbox(frame, height=200, state="disabled")
        self.participants_listbox.pack(pady=10, fill="both", expand=True)

        ctk.CTkButton(frame, text="View Future Excursions", command=self.view_future_excursions).pack(pady=5)

    def save_excursion(self):
        name = self.excursion_name_entry.get()
        date = self.excursion_date_entry.get_date().strftime("%Y-%m-%d")
        with open('excursions.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, date])
        self.excursion_name_entry.delete(0, 'end')
        self.excursion_date_entry.set_date(datetime.now())
        self.update_excursion_combobox()
        self.refresh_excursions()

    def save_participant(self):
        name = self.participant_name_entry.get()
        surname = self.participant_surname_entry.get()
        phone = self.participant_phone_entry.get()
        excursion = self.excursion_combobox.get()
        with open('participants.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, surname, phone, excursion])
        self.participant_name_entry.delete(0, 'end')
        self.participant_surname_entry.delete(0, 'end')
        self.participant_phone_entry.delete(0, 'end')

    def search_excursion(self):
        search_term = self.search_excursion_entry.get()
        self.excursion_listbox.configure(state="normal")
        self.excursion_listbox.delete('1.0', 'end')
        with open('participants.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if search_term.lower() in row[3].lower():
                    self.excursion_listbox.insert('end', f"{row[0]} {row[1]} - {row[2]}\n")
        self.excursion_listbox.configure(state="disabled")

    def search_participants_by_name(self):
        name_search = self.search_name_entry.get().lower()
        self.participants_listbox.configure(state="normal")
        self.participants_listbox.delete('1.0', 'end')
        with open('participants.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if name_search in row[0].lower() or name_search in row[1].lower():
                    self.participants_listbox.insert('end', f"{row[0]} {row[1]} - {row[2]} - {row[3]}\n")
        self.participants_listbox.configure(state="disabled")

    def search_participants_by_date(self):
        date_search = self.search_date_entry.get_date().strftime("%Y-%m-%d")
        self.participants_listbox.configure(state="normal")
        self.participants_listbox.delete('1.0', 'end')
        with open('excursions.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == date_search:
                    self.participants_listbox.insert('end', f"Excursion on {row[1]}: {row[0]}\n")
                    self.add_participants_for_excursion(row[0])
        self.participants_listbox.configure(state="disabled")

    def add_participants_for_excursion(self, excursion_name):
        with open('participants.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[3] == excursion_name:
                    self.participants_listbox.insert('end', f"  {row[0]} {row[1]} - {row[2]}\n")

    def view_future_excursions(self):
        self.participants_listbox.configure(state="normal")
        self.participants_listbox.delete('1.0', 'end')
        today = datetime.now().date()
        try:
            with open('excursions.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) >= 2:  # Ensure the row has at least 2 elements
                        try:
                            excursion_date = datetime.strptime(row[1], "%Y-%m-%d").date()
                            if excursion_date > today:
                                self.participants_listbox.insert('end', f"Future Excursion: {row[0]} on {row[1]}\n")
                        except ValueError as e:
                            print(f"Error parsing date for row {row}: {e}")
                    else:
                        print(f"Skipping invalid row: {row}")
        except FileNotFoundError:
            self.participants_listbox.insert('end', "Excursions file not found.\n")
        except Exception as e:
            self.participants_listbox.insert('end', f"An error occurred: {e}\n")
        self.participants_listbox.configure(state="disabled")

    def get_excursion_names(self):
        names = []
        try:
            with open('excursions.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if row:  # Check if row is not empty
                        names.append(row[0])
        except FileNotFoundError:
            print("Excursions file not found. Creating a new one.")
            self.create_csv_files()
        except Exception as e:
            print(f"An error occurred while reading excursions: {e}")
        return names

    def get_all_excursions(self):
        excursions = []
        try:
            with open('excursions.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if row:  # Check if row is not empty
                        excursions.append(f"{row[0]} - {row[1]}")
        except FileNotFoundError:
            print("Excursions file not found. Creating a new one.")
            self.create_csv_files()
        except Exception as e:
            print(f"An error occurred while reading excursions: {e}")
        return sorted(excursions, key=lambda x: datetime.strptime(x.split(' - ')[1], "%Y-%m-%d"), reverse=True)

    def update_excursion_combobox(self):
        self.excursion_combobox.configure(values=self.get_excursion_names())

    def refresh_excursions(self):
        self.all_excursions_dropdown.configure(values=self.get_all_excursions())

if __name__ == "__main__":
    app = ExcursionApp()
    app.mainloop()