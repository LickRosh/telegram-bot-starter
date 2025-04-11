import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import openai

# Загрузка переменных из Railway
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")

openai.api_key = OPENAI_API_KEY

# Функция для работы с GPT
async def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты чемодан без ручки. Ироничный, но полезный. Помогаешь людям не попасться на мошенников."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❗️ Ошибка OpenAI: {e}")
        return "⚠️ Чемодан застыл. Что-то пошло не так."

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    print(f"📨 Пользователь написал: {user_input}")
    reply = await ask_gpt(user_input)
    await update.message.reply_text(f"📦 Чемодан отвечает:\n\n{reply}")

# Запуск приложения с Webhook
def main():
    print("📦 Чемодан запускается через webhook...")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=f"{WEBHOOK_DOMAIN}/webhook"
    )

if __name__ == "__main__":
    main()
