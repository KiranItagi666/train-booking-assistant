from datetime import date, timedelta
import pandas as pd

# Read booked tickets
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

    # Monday -> BGM to SBC
    if current.weekday() == 0:
        if (current, "BGM-SBC") not in booked:
            missing.append(
                f"❌ {current} BGM -> SBC"
            )

    # Thursday -> SBC to BGM
    if current.weekday() == 3:
        if (current, "SBC-BGM") not in booked:
            missing.append(
                f"❌ {current} SBC -> BGM"
            )

    current += timedelta(days=1)

print("\n🚆 Train Booking Status\n")

if missing:
    print("Missing Bookings:\n")
    for item in missing:
        print(item)
else:
    print("✅ All bookings present for next 60 days")