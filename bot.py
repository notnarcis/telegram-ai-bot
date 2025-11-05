import os
from dotenv import load_dotenv
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import pytz

# Загружаем секреты из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("7993597120:AAHGE66WY_ktH64jb1UP9AUQDEzll9LIerk")
OPENAI_API_KEY = os.getenv("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")

openai.api_key = OPENAI_API_KEY

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я AI-бот. Напиши мне что-нибудь, и я отвечу.")

# Основной обработчик сообщений
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Произошла ошибка: {e}"

    await update.message.reply_text(reply)

def main():
    # Создаем приложение
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Явно задаем таймзону для JobQueue, чтобы избежать ошибки
    app.job_queue._scheduler.timezone = pytz.utc

    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    main()
