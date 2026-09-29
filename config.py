import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# معرف Telegram المسموح له بالتحكم في البوت
ALLOWED_USER_ID = int(os.environ["ALLOWED_USER_ID"])

MAX_ACTIONS_PER_RUN = int(
    os.getenv("MAX_ACTIONS_PER_RUN", "10")
)

WAIT_BETWEEN_ACTIONS = int(
    os.getenv("WAIT_BETWEEN_ACTIONS", "6")
)

DATABASE_FILE = os.getenv(
    "DATABASE_FILE",
    "cleaner.db"
)
