from gmail_reader import (
    get_gmail_service,
    get_irctc_emails,
    get_email_details,
    get_subject,
    decode_email_body
)

from irctc_parser import parse_irctc_email


def get_bookings():

    service = get_gmail_service()

    messages = get_irctc_emails(
        service,
        max_results=100
    )

    bookings = []

    for msg in messages:

        email = get_email_details(
            service,
            msg["id"]
        )

        subject = get_subject(
            email
        )

        if (
            "Booking Confirmation on IRCTC"
            not in subject
        ):
            continue

        html = decode_email_body(
            email
        )

        booking = parse_irctc_email(
            subject,
            html
        )

        if booking:
            bookings.append(
                booking
            )

    bookings.sort(
        key=lambda x: x["date"]
    )

    return bookings


def print_bookings(bookings):

    print("\nBookings Found\n")

    for booking in bookings:

        print("-" * 60)

        print(
            f"Date    : {booking.get('date', '')}"
        )

        print(
            f"Route   : {booking.get('route', '')}"
        )

        print(
            f"Train   : {booking.get('train', '')}"
        )

        print(
            f"Class   : {booking.get('class', '')}"
        )

        print(
            f"PNR     : {booking.get('pnr', '')}"
        )

        print(
            f"Status  : {booking.get('status', '')}"
        )

        print(
            f"Coach   : {booking.get('coach', '')}"
        )

        print(
            f"Berth   : {booking.get('berth', '')}"
        )

    print("\n")
    print(
        f"Total Bookings: {len(bookings)}"
    )


def main():

    bookings = get_bookings()

    print_bookings(
        bookings
    )


if __name__ == "__main__":
    main()