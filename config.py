import os

ZOHO_EMAIL = os.environ.get("ZOHO_EMAIL", "mahayla@zuldeirasystems.com")
ZOHO_APP_PASSWORD = os.environ.get("ZOHO_APP_PASSWORD", "3j8DcMP3g34e")
SMTP_HOST = "smtp.zoho.com"
SMTP_PORT = 587

SEED_ADDRESSES = [
    "mahaylabalentine04@gmail.com",
    "balentine.mahayla@outlook.com",
    "steve.charles11@outlook.com",
    "admin@zuldeira.com",
    "admin@caytral.com",
    "catherinebalentine109@gmail.com",
]

RAMP_SCHEDULE = {
    1: 3,
    2: 6,
    3: 12,
    4: 20,
    5: 40,
}
DEFAULT_DAILY_LIMIT = 40

LOG_FILE = "log.json"
