from gmail_reader import (
    GmailAuthError,
    get_gmail_service,
    get_irctc_emails,
    get_email_details,
    get_subject,
    decode_email_body
)

from irctc_parser import parse_irctc_email


def get_bookings():

    try:
        service = get_gmail_service()
    except GmailAuthError as exc:
        print(f"Gmail authentication unavailable: {exc}")
        return []

    messages = get_irctc_emails(
        service,
        max_results=100
    )

    bookings = []

    for msg in messages:

        try:
            email = get_email_details(
                service,
                msg["id"]
            )

            subject = get_subject(
                email
            )

            if "Booking Confirmation on IRCTC" not in subject:
                continue

            html = decode_email_body(
                email
            )

            booking = parse_irctc_email(
                subject,
                html
            )

            if not booking:
                print(f"Skipping email - parser returned None")
                continue

            if "date" not in booking:
                print(f"Skipping malformed booking (missing date):")
                print(booking)
                continue

            bookings.append(
                booking
            )

        except Exception as exc:
            print(f"Error parsing email {msg.get('id')}: {exc}")

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

    print()
    print(f"Total Bookings: {len(bookings)}")


def main():

    bookings = get_bookings()

    print_bookings(
        bookings
    )


if __name__ == "__main__":
    main()
