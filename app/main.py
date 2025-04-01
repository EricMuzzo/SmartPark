from nicegui import ui
from ui.pages.landing import landing_page
from ui.pages.login import login_page
from ui.pages.signup import signup_page
from ui.pages.overview import overview_page
from ui.pages.my_reservations import my_reservations_page
from api.client import ParkingAPIClient

#global api instance
api_client = ParkingAPIClient()

current_user_id = None
def session_login_page():
    global current_user_id
    login_page(api_client, lambda user_id: globals().update({"current_user_id": user_id}))

def session_signup_page():
    global current_user_id
    signup_page(api_client, lambda user_id: globals().update({"current_user_id": user_id}))
    
#Define routes
ui.page("/")(landing_page)
ui.page("/login")(session_login_page)
ui.page("/signup")(session_signup_page)
ui.page("/overview")(lambda: overview_page(api_client, current_user_id))
ui.page("/my_reservations")(lambda: my_reservations_page(api_client, current_user_id))

ui.run(host="0.0.0.0", port=80, title="Smart Parking System", reload=True)