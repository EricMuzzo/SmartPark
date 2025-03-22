def user_serial(user: dict) -> dict:
    """Transform a MongoDB document into a dict matching the user Schema"""
    return{
        "id": str(user["_id"]),
        "user_name": user["user_name"],
        "name": user["name"],
        "email": user["email"],
        "payment_card": user["payment_card"],
        "card_expiry_date": user["card_expiry_date"],
    }

# def users_serial(users) -> list:
#     """Transform multiple MongoDB documents into a list of dicts matching the user Schema"""
#     return[user_serial(user) for user in users]