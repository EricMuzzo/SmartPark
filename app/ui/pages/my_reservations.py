from nicegui import ui
from datetime import datetime
from api.client import ParkingAPIClient

def my_reservations_page(api_client: ParkingAPIClient, user_id: str):
    if not user_id:
        ui.notify("Please log in to view this page", type="negative")
        ui.navigate.to("/login")
        return

    def fetch_reservations():
        try:
            reservations_res = api_client.get_reservations({"user_id": ("eq", user_id)})
            return reservations_res
        except Exception as e:
            ui.notify(f"Failed to load reservations: {str(e)}", type="negative")
            return []

    #menu bar
    with ui.header().classes("flex items-center justify-between"):
        with ui.button(icon="menu").classes("ml-2"):
            with ui.menu() as menu:
                ui.menu_item("View Parking", lambda: ui.navigate.to("/overview")).classes("text-base")
                ui.menu_item("My Reservations", lambda: ui.navigate.to("/my_reservations")).classes("text-base")
                ui.menu_item("Log Out", lambda: [globals().update({"current_user_id": None}), ui.navigate.to("/")]).classes("text-base")
        ui.label("Smart Parking System").classes("text-2xl font-bold")

    @ui.refreshable
    def render_content():
        reservations_res = fetch_reservations()
        reservations = reservations_res.records
        with ui.column().classes("w-full max-w-4xl mx-auto p-4"):
            ui.label("My Reservations").classes("text-3xl font-bold mb-6 text-center")
            if not reservations:
                ui.label("No reservations found.").classes("text-lg text-gray-500")
            else:
                with ui.card().classes("w-full"):
                    for reservation in reservations:
                        with ui.row().classes("border-b border-gray-200 py-2 items-center"):
                            ui.label(f"Spot ID: {reservation.spot_id}").classes("text-base mr-4")
                            ui.label(f"Start: {datetime.fromisoformat(reservation.start_time).strftime('%Y-%m-%d %H:%M')}").classes("text-base mr-4")
                            ui.label(f"End: {datetime.fromisoformat(reservation.end_time).strftime('%Y-%m-%d %H:%M')}").classes("text-base mr-4")
                            ui.label(f"Cost: ${reservation.final_price:.2f}").classes("text-base mr-4")
                            ui.space()
                            ui.button(
                                "Delete",
                                on_click=lambda r=reservation: handle_delete(r._id)
                            ).classes("bg-red-500 text-white")

    def handle_delete(reservation_id: str):
        try:
            if api_client.delete_reservation(reservation_id):
                ui.notify("Reservation deleted successfully!", type="positive")
                render_content.refresh()
            else:
                ui.notify("Failed to delete reservation", type="negative")
        except Exception as e:
            ui.notify(f"Error deleting reservation: {str(e)}", type="negative")

    render_content()