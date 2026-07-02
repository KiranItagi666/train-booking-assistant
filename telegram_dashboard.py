from telegram import Bot
import asyncio
import os

from gmail_bookings import get_bookings
from travel_dashboard import build_dashboard

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")


async def send_dashboard():

    bookings = get_bookings()

    dashboard = build_dashboard(
        bookings
    )

    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram credentials not configured; skipping send.")
        return

    try:
        bot = Bot(
            token=BOT_TOKEN
        )

        await bot.send_message(
            chat_id=CHAT_ID,
            text=dashboard
        )
    except Exception as exc:
        print(f"⚠️ Failed to send Telegram dashboard: {exc}")
        return

    print(
        "✅ Dashboard sent successfully"
    )


asyncio.run(
    send_dashboard()
)