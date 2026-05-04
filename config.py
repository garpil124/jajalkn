import os
from dotenv import load_dotenv

load_dotenv()  # 🔥 WAJIB biar .env kebaca

# ================= ENV SAFE =================
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

API_URL = os.getenv("API_URL", "http://127.0.0.1:5000/get")

# ================= OWNER =================
OWNER_IDS = list(map(int, os.getenv("OWNER_IDS", "8209644174,5744453710").split(",")))

# ================= GROUP =================
TARGET_CHATS = [-1002101188966]
FORCE_GROUP = -1002101188966
FORCE_LINK = "https://t.me/tongkrongan_gaje"

# ================= FILE PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PARTNER_FILE = os.path.join(BASE_DIR, "partner.json")
SETTING_FILE = os.path.join(BASE_DIR, "setting.json")
QUEUE_FILE = os.path.join(BASE_DIR, "queue.json")
AUTO_TAG_FILE = os.path.join(BASE_DIR, "autotag.json")
BUTTON_FILE = os.path.join(BASE_DIR, "buttons.json")

# ================= OTHER =================
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
SERVICE_NAME = "partnerbot"
