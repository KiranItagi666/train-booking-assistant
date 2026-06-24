from telegram import Bot
import pandas as pd
from datetime import date, timedelta
import asyncio
import os

# =========================
# CONFIGURATION
# =========================

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# =========================
# READ BOOKINGS
# =========================

df = pd.read_csv("bookings.csv")

booked = set(
    zip(
        pd.to_datetime(df["date"]).dt.date,
        df["route"]
    )
)

# =========================
# CHECK FUTURE BOOKINGS
# =========================

today = date.today()

# Check trips 50–70 days ahead
start_date = today + timedelta(days=50)
end_date = today + timedelta(days=70)

missing = []

current = start_date

while current <= end_date:

    # Monday: Belagavi -> Bangalore
    if current.weekday() == 0:
        if (current, "BGM-SBC") not in booked:
            missing.append(
                f"❌ {current} BGM → SBC"
            )

    # Thursday: Bangalore -> Belagavi
    if current.weekday() == 3:
        if (current, "SBC-BGM") not in booked:
            missing.append(
                f"❌ {current} SBC → BGM"
            )

    current += timedelta(days=1)

# =========================
# BUILD MESSAGE
# =========================

message = "🚆 Train Booking Status\n\n"

if missing:
    message += "Missing Bookings:\n\n"
    message += "\n".join(missing)
else:
    message += "✅ All bookings present for the booking window."

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

print("✅ Telegram notification sent successfully!")