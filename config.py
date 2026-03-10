import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID")  # We'll need to set this later
DB_PATH = os.getenv("DB_PATH", "applications.db")

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided in .env file.")
