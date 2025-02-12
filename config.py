# Flask configuration
DEBUG = True
SECRET_KEY = 'your_secret_key'

# Database configuration
DATABASE_URI = 'sqlite:///lady_essence.db'

# Twilio configuration (for SMS notifications)
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# SMTP configuration (for email notifications)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@gmail.com'
SMTP_PASSWORD = 'your_email_password'

# Redis configuration (for caching)
REDIS_URL = 'redis://localhost:6379/0'