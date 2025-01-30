from datetime import datetime
import sqlite3
import requests

def get_db_connection():
    conn = sqlite3.connect("menstrual_tracker.db")
    conn.row_factory = sqlite3.Row
    return conn

def save_meal(phone_number, meal):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO meal_history (phone_number, meal, date)
        VALUES (?, ?, ?)
    """, (phone_number, meal, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_meal_history(phone_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT meal FROM meal_history WHERE phone_number = ? ORDER BY date DESC LIMIT 5
    """, (phone_number,))
    meals = [row[0] for row in cursor.fetchall()]
    conn.close()
    return meals

def get_nutrition_guidance(meal_history):
    response = requests.post(
        "https://gemini-api.com/nutrition-guidance",
        json={"meal_history": meal_history}
    )
    return response.json().get("recommendation", "No recommendation available.")