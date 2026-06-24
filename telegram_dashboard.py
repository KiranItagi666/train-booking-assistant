from telegram import Bot
import asyncio
import os

from gmail_bookings import get_bookings
from travel_dashboard import build_dashboard

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


async def send_dashboard():

    bookings = get_bookings()

    dashboard = build_dashboard(
        bookings
    )

    bot = Bot(
        token=BOT_TOKEN
    )

    await bot.send_message(
        chat_id=CHAT_ID,
        text=dashboard
    )

    print(
        "✅ Dashboard sent successfully"
    )


asyncio.run(
    send_dashboard()
)