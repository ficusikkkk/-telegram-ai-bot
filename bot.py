import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message or not message.text:
        return

    bot_username = context.bot.username

    # Отвечаем только на сообщения с упоминанием бота
    if f"@{bot_username.lower()}" not in message.text.lower():
        return

    question = message.text.replace(f"@{bot_username}", "").strip()

    if not question:
        await message.reply_text("Напиши вопрос после упоминания меня 🙂")
        return

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=(
                "Ты полезный AI-помощник в Telegram-группе. "
                "Отвечай понятно, кратко и по существу. "
                "Отвечай на языке пользователя."
            ),
            input=question
        )

        await message.reply_text(response.output_text)

    except Exception as e:
        print(f"Error: {e}")
        await message.reply_text(
            "Не удалось получить ответ. Попробуй ещё раз."
        )


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            answer
        )
    )

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
