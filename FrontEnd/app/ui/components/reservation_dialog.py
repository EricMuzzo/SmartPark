from nicegui import ui
from api.client import ParkingAPIClient, PricingAPIClient
from api.models import ReservationCreate, ParkingSpot
from datetime import datetime, timedelta

def reservation_dialog(api_client: ParkingAPIClient, spot: ParkingSpot, user_id: str, on_success):
    """Opens a dialog to create a reservation for a given spot."""
    with ui.dialog() as dialog, ui.card().classes("w-96"):
        ui.label(f"Reserve Spot {spot.spot_number} on Floor {spot.floor_level}").classes("text-xl font-bold mb-4")
        
        start_time = ui.input("Start Time", value=(datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M")).props("type=datetime-local").classes("w-full mb-4")
        end_time = ui.input("End Time", value=(datetime.now() + timedelta(hours=1, minutes=5)).strftime("%Y-%m-%dT%H:%M")).props("type=datetime-local").classes("w-full mb-4")
        
        # Reactive price display
        @ui.refreshable
        def price_display():
            try:
                pricer = PricingAPIClient()
                start_dt = datetime.fromisoformat(start_time.value.replace("T", " "))
                end_dt = datetime.fromisoformat(end_time.value.replace("T", " "))
                price = pricer.fetch_total_price(start_dt, end_dt)
                ui.label(f"Estimated Price: ${price:.2f}").classes("text-base mb-4")
            except Exception:
                ui.label("Estimated Price: $0.00 (invalid time)").classes("text-base mb-4 text-gray-500")

        # Initial render of price
        price_display()

        # Update price on input change
        start_time.on("change", price_display.refresh)
        end_time.on("change", price_display.refresh)

        def handle_reserve():

            if not start_time.value or not end_time.value:
                ui.notify("Please fill in both start and end times", type="negative")
                return
            
            try:
                start_dt = datetime.fromisoformat(start_time.value.replace("T", " "))
                end_dt = datetime.fromisoformat(end_time.value.replace("T", " "))
                
                if end_dt <= start_dt:
                    ui.notify("End time must be after start time", type="negative")
                    return


                reservation = ReservationCreate(
                    user_id=user_id,
                    spot_id=spot._id,
                    start_time=start_dt.isoformat(),
                    end_time=end_dt.isoformat()
                )
                api_client.create_reservation(reservation)
                ui.notify(f"Spot {spot.spot_number} reserved successfully!", type="positive")
                dialog.close()
                on_success()  #callback for refresh
            except Exception as e:
                ui.notify(f"Failed to reserve spot: {str(e)}", type="negative")

        with ui.row().classes("w-full justify-end"):
            ui.button("Cancel", on_click=dialog.close).classes("bg-gray-500 text-white")
            ui.button("Reserve", on_click=handle_reserve).classes("bg-blue-500 text-white")

    dialog.open()