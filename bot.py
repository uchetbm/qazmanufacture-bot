import os
import re
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import gspread
from google.oauth2.service_account import Credentials
import json

# Настройки
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GOOGLE_CREDS = os.environ.get("GOOGLE_CREDENTIALS")
SHEET_ID = "1sZ13y9C5-8R4Bd3ZngM5hFySo43AGjv9jyu2grwv_pw"

def get_sheet():
    creds_dict = json.loads(GOOGLE_CREDS)
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user.first_name or "Unknown"
    
    try:
        sheet = get_sheet()
        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            str(update.effective_chat.id),
            user,
            text
        ])
        print(f"Записано: {text[:50]}...")
    except Exception as e:
        print(f"Ошибка: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
