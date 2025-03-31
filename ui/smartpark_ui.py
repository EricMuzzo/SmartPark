import tkinter as tk
from tkinter import messagebox
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

class SmartParkUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Parking System")
        self.root.geometry("450x650")
        self.root.configure(bg="#f0f4f8")  # Light gray background

        # Main Frame
        main_frame = tk.Frame(root, bg="#f0f4f8", padx=20, pady=20)
        main_frame.pack(expand=True)

        # Title
        title_label = tk.Label(
            main_frame, 
            text="Smart Parking Reservation", 
            font=("Helvetica", 18, "bold"), 
            bg="#f0f4f8", 
            fg="#2c3e50"  # Dark blue
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Form Frame
        form_frame = tk.Frame(main_frame, bg="#ffffff", padx=15, pady=15, relief="flat", bd=2)
        form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        form_frame.configure(highlightbackground="#dcdcdc", highlightthickness=1)  # Subtle border

        # Labels and Entries
        label_font = ("Helvetica", 11)
        entry_font = ("Helvetica", 10)

        # User Name
        tk.Label(form_frame, text="User Name:", font=label_font, bg="#ffffff", fg="#34495e").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form_frame, width=30, font=entry_font, relief="flat", bg="#ecf0f1", fg="#2c3e50")
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)
        self.name_entry.insert(0, "testuser")

        # Parking Number
        tk.Label(form_frame, text="Parking Number:", font=label_font, bg="#ffffff", fg="#34495e").grid(row=1, column=0, sticky="w", pady=5)
        self.parking_entry = tk.Entry(form_frame, width=30, font=entry_font, relief="flat", bg="#ecf0f1", fg="#2c3e50")
        self.parking_entry.grid(row=1, column=1, pady=5, padx=5)
        self.parking_entry.insert(0, "A1")

        # Floor Number
        tk.Label(form_frame, text="Floor Number:", font=label_font, bg="#ffffff", fg="#34495e").grid(row=2, column=0, sticky="w", pady=5)
        self.floor_entry = tk.Entry(form_frame, width=30, font=entry_font, relief="flat", bg="#ecf0f1", fg="#2c3e50")
        self.floor_entry.grid(row=2, column=1, pady=5, padx=5)
        self.floor_entry.insert(0, "1")

        # Start Time
        tk.Label(form_frame, text="Start Time (YYYY-MM-DDTHH:MM:SS):", font=label_font, bg="#ffffff", fg="#34495e").grid(row=3, column=0, sticky="w", pady=5)
        self.start_entry = tk.Entry(form_frame, width=30, font=entry_font, relief="flat", bg="#ecf0f1", fg="#2c3e50")
        self.start_entry.grid(row=3, column=1, pady=5, padx=5)
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        self.start_entry.insert(0, start_time.strftime("%Y-%m-%dT%H:%M:%S"))

        # End Time
        tk.Label(form_frame, text="End Time (YYYY-MM-DDTHH:MM:SS):", font=label_font, bg="#ffffff", fg="#34495e").grid(row=4, column=0, sticky="w", pady=5)
        self.end_entry = tk.Entry(form_frame, width=30, font=entry_font, relief="flat", bg="#ecf0f1", fg="#2c3e50")
        self.end_entry.grid(row=4, column=1, pady=5, padx=5)
        end_time = start_time + timedelta(hours=2)
        self.end_entry.insert(0, end_time.strftime("%Y-%m-%dT%H:%M:%S"))

        # Buttons Frame
        button_frame = tk.Frame(main_frame, bg="#f0f4f8", pady=10)
        button_frame.grid(row=2, column=0, columnspan=2)

        tk.Button(
            button_frame, 
            text="Submit",
            command=self.submit_data,
            bg="#3498db",  # Blue
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat", 
            padx=20, 
            pady=5
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame, 
            text="Reserve", 
            command=self.reserve_parking, 
            bg="#2ecc71",  # Green
            fg="white", 
            font=("Helvetica", 11, "bold"), 
            relief="flat", 
            padx=20, 
            pady=5
        ).pack(side="left", padx=10)

        # Response Display
        self.response_text = tk.Text(main_frame, height=10, width=40, font=("Helvetica", 10), bg="#ffffff", fg="#2c3e50", relief="flat")
        self.response_text.grid(row=3, column=0, columnspan=2, pady=10)
        self.response_text.configure(highlightbackground="#dcdcdc", highlightthickness=1)

    def get_user_id(self, name):
        """Create a user via POST /auth/signup and return their user_id."""
        signup_data = {
            "username": name.lower().replace(" ", ""),
            "name": name,
            "email": f"{name.lower().replace(' ', '')}@example.com",
            "password": "password123"  # Should be user-input in a real app
        }
        try:
            response = requests.post(
                f"{API_BASE_URL}auth/signup",
                headers={"Content-Type": "application/json"},
                data=json.dumps(signup_data)
            )
            response.raise_for_status()
            return response.json()["_id"]  # Assumes _id is returned
        except requests.exceptions.RequestException as e:
            error_msg = f"Signup Error: {e.response.status_code} - {e.response.text}"
            self.response_text.insert(tk.END, error_msg + "\n")
            return None

    def get_spot_id(self, parking_num, floor_num):
        """Find a spot_id matching parking_number and floor_number via GET /spots."""
        try:
            response = requests.get(f"{API_BASE_URL}spots")
            response.raise_for_status()
            spots = response.json()
            for spot in spots:
                if (str(spot["spot_number"]) == str(parking_num) and 
                    str(spot["floor_level"]) == str(floor_num) and 
                    spot["status"] == "vacant"):
                    return spot["_id"]
            self.response_text.insert(tk.END, "No vacant spot found for that parking number and floor!\n")
            return None
        except requests.exceptions.RequestException as e:
            error_msg = f"Spots Error: {e.response.status_code} - {e.response.text}"
            self.response_text.insert(tk.END, error_msg + "\n")
            return None

    def submit_data(self):
        """Display the entered data in the text box."""
        name = self.name_entry.get()
        parking_num = self.parking_entry.get()
        floor_num = self.floor_entry.get()
        start_time = self.start_entry.get()
        end_time = self.end_entry.get()

        if not all([name, parking_num, floor_num, start_time, end_time]):
            messagebox.showerror("Error", "All fields are required!")
            return

        response = f"Name: {name}\nParking: {parking_num}\nFloor: {floor_num}\nStart: {start_time}\nEnd: {end_time}"
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, response + "\n")

    def reserve_parking(self):
        """Reserve a parking spot via POST /reservations."""
        name = self.name_entry.get()
        parking_num = self.parking_entry.get()
        floor_num = self.floor_entry.get()
        start_time = self.start_entry.get()
        end_time = self.end_entry.get()

        if not all([name, parking_num, floor_num, start_time, end_time]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Get user_id
        user_id = self.get_user_id(name)
        if not user_id:
            return

        # Get spot_id
        spot_id = self.get_spot_id(parking_num, floor_num)
        if not spot_id:
            return

        reservation_data = {
            "user_id": user_id,
            "spot_id": spot_id,
            "start_time": start_time,
            "end_time": end_time
        }

        try:
            response = requests.post(
                f"{API_BASE_URL}reservations",
                headers={"Content-Type": "application/json"},
                data=json.dumps(reservation_data)
            )
            response.raise_for_status()
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, f"Reservation successful!\n{response.text}\n")
        except requests.exceptions.RequestException as e:
            self.response_text.delete(1.0, tk.END)
            error_msg = f"Reservation Error: {e.response.status_code} - {e.response.text}"
            self.response_text.insert(tk.END, error_msg + "\n")

def main():
    root = tk.Tk()
    app = SmartParkUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()