import sqlite3
import requests

def fetch_nutrition_guidance(user_input):
    """
    Fetch guidance related to planetary care from an external API.

    Args:
        user_input (str): The keyword for the guidance (e.g., "nutrition").

    Returns:
        str: The fetched guidance or an error message if the request fails.
    """
    try:
        response = requests.get(f"https://api.gemin.com/nutrition?query={user_input}")
        if response.status_code == 200:
            return response.json().get("guidance", "Nta makuru aboneka.")
        else:
            return "Hari ikibazo mu kubona amakuru."
    except Exception as e:
        return "Ntibikunze kubona amakuru."

def save_planetary_guidance(phone_number, guidance):
    """
    Save the fetched planetary guidance to the database.

    Args:
        phone_number (str): The user's phone number.
        guidance (str): The fetched guidance text.
    """
    conn = sqlite3.connect("menstrual_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO planetary_guidance (phone_number, guidance)
        VALUES (?, ?)
    """, (phone_number, guidance))
    conn.commit()
    conn.close()
