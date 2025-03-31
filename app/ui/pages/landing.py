from nicegui import ui

def landing_page():
    with ui.column().classes("w-full max-w-md mx-auto p-4 flex flex-col items-center justify-center min-h-screen"):
        ui.label("Smart Parking System").classes("text-3xl font-bold mb-8 text-center")
        ui.button("Login", on_click=lambda: ui.navigate.to("/login")).classes("w-48 mb-4 bg-blue-500 text-white")
        ui.button("Sign Up", on_click=lambda: ui.navigate.to("/signup")).classes("w-48 bg-green-500 text-white")