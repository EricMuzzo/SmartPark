from nicegui import ui
from collections import defaultdict
from api.client import ParkingAPIClient, PricingAPIClient
from ui.components.reservation_dialog import reservation_dialog
from datetime import datetime

current_user_id = None

def overview_page(api_client: ParkingAPIClient, user_id: str):
    if not user_id:
        ui.notify("Please log in to view this page", type="negative")
        ui.navigate.to("/login")
        return
    
    def fetch_spots():
        try:
            return api_client.get_spots()
        except Exception as e:
            ui.notify(f"Failed to load spots: {str(e)}", type="negative")
            return []
        
    with ui.header().classes("flex items-center justify-between"):
        with ui.button(icon="menu").classes("ml-2"):
            with ui.menu() as menu:
                ui.menu_item("View Parking", lambda: ui.navigate.to("/overview")).classes("text-base")
                ui.menu_item("My Reservations", lambda: ui.navigate.to("/my_reservations")).classes("text-base")
                ui.menu_item("Log Out", lambda: [globals().update({"current_user_id": None}), ui.navigate.to("/")]).classes("text-base")
        ui.label("Smart Parking System").classes("text-2xl font-bold")
    
    @ui.refreshable
    def render_content():
        spots_response = fetch_spots()
        
        spots = spots_response.records
        total_spots = spots_response.count
        total_available = sum(1 for spot in spots if spot.status == "vacant")
        total_occupied = sum(1 for spot in spots if spot.status == "occupied")
        
        pricer = PricingAPIClient()
        price_per_minute = pricer.fetch_rate(datetime.now())

        spots_by_floor = defaultdict(list)
        for spot in spots:
            spots_by_floor[spot.floor_level].append(spot)

        with ui.column().classes("w-full items-center max-w-4xl mx-auto p-4"):
            ui.label("Parking Overview").classes("text-3xl font-bold mb-6 text-center")
            with ui.card().classes("w-full mb-8"):
                ui.label(f"Total Spots: {total_spots}").classes("text-lg")
                ui.label(f"Available Spots: {total_available}").classes("text-lg text-green-600")
                ui.label(f"Occupied Spots: {total_occupied}").classes("text-lg text-red-600")
                ui.label(f"Price Rate: ${price_per_minute:.2f} per minute").classes("text-lg")

            ui.label("Floor Levels").classes("text-2xl font-bold mb-4")
            for floor in sorted(spots_by_floor.keys()):
                with ui.expansion(f"Floor {floor}", icon="floor").classes("w-full mb-2 text-xl border border-gray-300"):

                    ui.query(".q-expansion-item__header").classes("font-extrabold text-lg")
                    
                    for spot in spots_by_floor[floor]:
                        with ui.row().classes("w-full border border-gray-200 p-2 items-center"):
                            
                            if spot.status == "vacant":
                                style = "text-base mr-4 border border-green-200 bg-green-300 p-1"
                            else:    
                                style = "text-base mr-4 border border-red-400 bg-red-500 p-1"
                                
                            ui.label(f"Spot {spot.spot_number}").classes("font-semibold text-base mr-4")
                            ui.label(spot.status.capitalize()).classes(style)
                            ui.space()  # Pushes the button to the far right
                            
                            reserve_button = ui.button("Reserve").classes("text-white")
                            if spot.status == "vacant":
                                reserve_button.classes("bg-blue-500").on("click", lambda spot=spot: reservation_dialog(api_client, spot, user_id, lambda: render_content.refresh()))
                            else:
                                reserve_button.classes("bg-gray-400").disable()

            ui.button("Back to Home", on_click=lambda: ui.navigate.to("/")).classes("mt-4 bg-gray-500 text-white")
            
    render_content()