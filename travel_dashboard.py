from gmail_bookings import get_bookings
from datetime import datetime, date, timedelta


DASHBOARD_WIDTH = 50


def get_status_icon(status):

    status = status.upper()

    if "CNF" in status:
        return "🟢"

    if "RAC" in status:
        return "🟡"

    if "WL" in status:
        return "🔴"

    return "⚪"


def get_upcoming_trips(bookings):

    today = date.today()

    upcoming = [
        booking
        for booking in bookings
        if datetime.strptime(
            booking["date"],
            "%Y-%m-%d"
        ).date() >= today
    ]

    return sorted(
        upcoming,
        key=lambda trip: trip["date"]
    )


def get_missing_bookings(bookings):

    if not bookings:
        return []

    booked_routes = {
        (
            booking["date"],
            booking["route"]
        )
        for booking in bookings
    }

    latest_booking_date = max(
        datetime.strptime(
            booking["date"],
            "%Y-%m-%d"
        ).date()
        for booking in bookings
    )

    start_date = latest_booking_date + timedelta(days=1)
    end_date = start_date + timedelta(days=40)

    missing = []

    current = start_date

    while current <= end_date:

        current_str = current.strftime(
            "%Y-%m-%d"
        )

        # Monday: Belagavi -> Bangalore
        if current.weekday() == 0:

            if (
                current_str,
                "BGM-SBC"
            ) not in booked_routes:

                missing.append(
                    {
                        "date": current_str,
                        "route": "BGM-SBC"
                    }
                )

        # Thursday: Bangalore -> Belagavi
        elif current.weekday() == 3:

            if (
                current_str,
                "SBC-BGM"
            ) not in booked_routes:

                missing.append(
                    {
                        "date": current_str,
                        "route": "SBC-BGM"
                    }
                )

        current += timedelta(days=1)

    return missing


def format_trip(trip):

    icon = get_status_icon(
        trip.get(
            "status",
            ""
        )
    )

    route = trip.get(
        "route",
        ""
    ).replace(
        "-",
        " → "
    )

    return [
        f"{icon} {trip.get('date', '')}",
        route,
        "",
        f"Train : {trip.get('train', '')}",
        f"PNR   : {trip.get('pnr', '')}",
        f"Class : {trip.get('class', '')}",
        "",
        f"Status: {trip.get('status', '')}",
        f"Coach : {trip.get('coach', '-')}",
        f"Berth : {trip.get('berth', '-')}"
    ]


def add_section(lines, title):

    lines.append("=" * DASHBOARD_WIDTH)
    lines.append(title)
    lines.append("=" * DASHBOARD_WIDTH)


def build_dashboard(bookings):

    upcoming = get_upcoming_trips(
        bookings
    )

    missing = get_missing_bookings(
        bookings
    )

    lines = []

    # Header

    lines.append(
        "🚆 Kiran Travel Dashboard"
    )

    lines.append("")

    # Next Booking

    if missing:

        next_trip = missing[0]

        lines.append(
            "🎯 NEXT BOOKING REQUIRED"
        )

        lines.append(
            f"{next_trip['date']} "
            f"{next_trip['route'].replace('-', ' → ')}"
        )

        lines.append("")

    # Upcoming Trips

    add_section(
        lines,
        "UPCOMING TRIPS"
    )

    if upcoming:

        for index, trip in enumerate(
            upcoming
        ):

            lines.extend(
                format_trip(trip)
            )

            if index < len(upcoming) - 1:

                lines.append("")
                lines.append(
                    "-" * DASHBOARD_WIDTH
                )

            lines.append("")

    else:

        lines.append(
            "No upcoming trips found"
        )

    # Missing Bookings

    add_section(
        lines,
        "MISSING BOOKINGS"
    )

    if missing:

        for trip in missing[:3]:

            lines.append(
                f"❌ {trip['date']} "
                f"{trip['route'].replace('-', ' → ')}"
            )

        remaining = len(missing) - 3

        if remaining > 0:

            lines.append("")
            lines.append(
                f"... and {remaining} more"
            )

    else:

        lines.append(
            "✅ No missing bookings"
        )

    # Summary

    lines.append("")

    add_section(
        lines,
        "SUMMARY"
    )

    lines.append(
        f"Upcoming Trips : {len(upcoming)}"
    )

    lines.append(
        f"Missing Trips  : {len(missing)}"
    )

    total = (
        len(upcoming)
        + len(missing)
    )

    if total > 0:

        coverage = (
            len(upcoming)
            / total
        ) * 100

        lines.append(
            f"Coverage       : "
            f"{coverage:.1f}%"
        )

    return "\n".join(lines)


def main():

    bookings = get_bookings()

    dashboard = build_dashboard(
        bookings
    )

    print()
    print(dashboard)
    print()


if __name__ == "__main__":
    main()