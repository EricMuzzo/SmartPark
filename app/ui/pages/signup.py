from nicegui import ui
from api.client import ParkingAPIClient
import requests

def signup_page(api_client: ParkingAPIClient, on_signup):

    with ui.column().classes("w-full max-w-md mx-auto p-4 flex flex-col items-center justify-center min-h-screen"):
        ui.label("Sign Up").classes("text-3xl font-bold mb-8 text-center")
        
        username = ui.input("Username", placeholder="Choose a username").props("outlined").classes("w-full mb-4")
        name = ui.input("Name", placeholder="Enter your full name").props("outlined").classes("w-full mb-4")
        email = ui.input("Email", placeholder="Enter your email").props("outlined").classes("w-full mb-4")
        password = ui.input("Password", placeholder="Choose a password").props("outlined type=password").classes("w-full mb-4")

        def handle_signup():

            if not all([username.value, name.value, email.value, password.value]):
                ui.notify("Please fill in all fields", type="negative")
                return

            try:
                result = api_client.signup(username.value, password.value, name.value, email.value)
                on_signup(result._id)
                ui.notify("Signup successful! You can now log in.", type="positive")
                ui.navigate.to("/overview")
            except requests.HTTPError as e:
                if e.response.status_code == 400:
                    ui.notify("Username or email already exists", type="negative")
                elif e.response.status_code == 500:
                    ui.notify("Server error. Please try again later.", type="negative")
                else:
                    ui.notify(f"Signup failed: {str(e)}", type="negative")
            except requests.exceptions.RequestException as e:
                ui.notify(f"Signup failed: {str(e)}", type="negative")

        ui.button("Sign Up", on_click=handle_signup).classes("w-48 bg-green-500 text-white mb-4")
        ui.button("Back to Home", on_click=lambda: ui.navigate.to("/")).classes("w-48 bg-gray-500 text-white")