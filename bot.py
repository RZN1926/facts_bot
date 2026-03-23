import json
import os
import random
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatMemberHandler, ContextTypes
from facts import *

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHATS_FILE = "chats.json"

# --- Работа с сохранёнными чатами ---

def load_chats():
    if not os.path.exists(CHATS_FILE):
        return []
    with open(CHATS_FILE, "r") as f:
        return json.load(f)

def save_chats(chats):
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f)

# --- Обработчик: бота добавили или удалили из группы ---

async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.my_chat_member
    chats = load_chats()

    if result.new_chat_member.status in ["member", "administrator"]:
        if result.chat.id not in chats:
            chats.append(result.chat.id)
            print(f"Добавлен в чат: {result.chat.id}")

    elif result.new_chat_member.status in ["left", "kicked"]:
        if result.chat.id in chats:
            chats.remove(result.chat.id)
            print(f"Удалён из чата: {result.chat.id}")

    save_chats(chats)

# --- Рассылка фактов ---

async def send_facts(app):
    while True:
        # Случайный интервал от 30 минут до 5 часов (в секундах)
        # interval = random.randint(1 * 60, 5 * 60 * 60)
        interval = random.randint(1, 5)
        await asyncio.sleep(interval)

        chats = load_chats()
        fact = random.choice(FACTS)
        facts_for_yaica = random.choice(FACTS_FOR_YAICA)

        for chat_id in chats:
            if chat_id == -1002932870411:
                try:
                    await app.bot.send_message(chat_id=chat_id, text=f"fffff")
                except Exception as e:
                    print(f"Ошибка отправки в яйца: {e}")
            else:
                try:
                    await app.bot.send_message(chat_id=chat_id, text=f"{fact}")
                except Exception as e:
                    print(f"Ошибка отправки в {chat_id}: {e}")

# --- Запуск ---

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))

    async with app:
        await app.start()
        await app.updater.start_polling()
        await send_facts(app)  # запускаем рассылку

if __name__ == "__main__":
    asyncio.run(main())
