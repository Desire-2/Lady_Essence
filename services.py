from datetime import datetime, timedelta
from twilio.rest import Client
import smtplib
import requests

# Calculate cycle dates
def calculate_cycle_dates(last_period_date, cycle_length):
    last_period = datetime.strptime(last_period_date, "%d/%m/%Y")
    next_period = last_period + timedelta(days=cycle_length)
    ovulation = next_period - timedelta(days=14)
    fertile_start = ovulation - timedelta(days=3)
    fertile_end = ovulation + timedelta(days=3)
    return next_period, ovulation, fertile_start, fertile_end

# Fetch nutrition guidance (mock function)
def fetch_nutrition_guidance(query):
    response = requests.get(f"https://api.nutritionix.com/v1/search/{query}")
    return response.json()

# Save meal (mock function)
def save_meal(phone_number, meal):
    pass

# Get meal history (mock function)
def get_meal_history(phone_number):
    return []

# Get nutrition guidance based on meal history (mock function)
def get_nutrition_guidance(meal_history):
    return "Increase your intake of fruits and vegetables."

# Send SMS using Twilio
def send_sms(phone_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )

# Send email using SMTP
def send_email(email, message):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, email, message)

def get_emergency_contacts():
    return "Kubuntu Helpline: 3029\nPolice: 112\nAmbulance: 912"

def get_health_tips(tip_id):
    tips = {
        '1': "Eat iron-rich foods like spinach during your period.",
        '2': "Light exercises like yoga reduce menstrual cramps.",
        '3': "Practice mindfulness for mental wellness."
    }
    return tips.get(tip_id, "Tip not found.")

def schedule_appointment(phone_number, issue):
    session = get_session()
    appointment = Appointment(
        phone_number=phone_number,
        issue=issue,
        timestamp=datetime.now()
    )
    session.add(appointment)
    session.commit()