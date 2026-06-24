from telegram import Bot
import pandas as pd
from datetime import date, timedelta
import asyncio

# =========================
# CONFIGURATION
# =========================

BOT_TOKEN = "8955527381:AAFrBzVlizMART5ywTXdLd0ZqIdlpsefyrQ"
CHAT_ID = "926596744"

# =========================
# CHECK BOOKINGS
# =========================

df = pd.read_csv("bookings.csv")

booked = set(
    zip(
        pd.to_datetime(df["date"]).dt.date,
        df["route"]
    )
)

today = date.today()
end_date = today + timedelta(days=60)

missing = []

current = today

while current <= end_date:

    # Monday
    if current.weekday() == 0:
        if (current, "BGM-SBC") not in booked:
            missing.append(f"❌ {current} BGM → SBC")

    # Thursday
    if current.weekday() == 3:
        if (current, "SBC-BGM") not in booked:
            missing.append(f"❌ {current} SBC → BGM")

    current += timedelta(days=1)

# =========================
# BUILD MESSAGE
# =========================

message = "🚆 Train Booking Status\n\n"

if missing:
    message += "Missing Bookings:\n\n"
    message += "\n".join(missing)
else:
    message += "✅ All bookings present for next 60 days"

# =========================
# SEND TO TELEGRAM
# =========================

async def send_message():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

asyncio.run(send_message())

print("Telegram notification sent successfully!")