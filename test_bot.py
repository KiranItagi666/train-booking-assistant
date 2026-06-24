from telegram import Bot
import asyncio

BOT_TOKEN = "8955527381:AAFrBzVlizMART5ywTXdLd0ZqIdlpsefyrQ"
CHAT_ID = "926596744"

async def main():
    bot = Bot(token=BOT_TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text="✅ Kiran Travel Assistant is working!"
    )

    print("Message sent successfully")

asyncio.run(main())