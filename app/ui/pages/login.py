from nicegui import ui
import requests
from api.client import ParkingAPIClient

def login_page(api_client: ParkingAPIClient, on_login):

    with ui.column().classes("w-full max-w-md mx-auto p-4 flex flex-col items-center justify-center min-h-screen"):
        ui.label("Login").classes("text-3xl font-bold mb-8 text-center")
        
        username = ui.input("Username", placeholder="Enter your username").props("outlined").classes("w-full mb-4")
        password = ui.input("Password", placeholder="Enter your password").props("outlined type=password").classes("w-full mb-4")

        def handle_login():
            #make sure fields are populated
            if not username.value or not password.value:
                ui.notify("Please fill in all fields", type="negative")
                return

            try:
                if api_client.login(username.value, password.value):
                    
                    user = api_client.get_users(username=username.value).records[0]
                    on_login(user._id)
                    ui.notify("Login successful!", type="positive")
                    ui.navigate.to("/overview")
                else:
                    ui.notify("Invalid username or password", type="negative")
            except requests.exceptions.RequestException as e:
                ui.notify(f"Login failed: {str(e)}", type="negative")

        ui.button("Login", on_click=handle_login).classes("w-48 bg-blue-500 text-white mb-4")
        ui.button("Back to Home", on_click=lambda: ui.navigate.to("/")).classes("w-48 bg-gray-500 text-white")