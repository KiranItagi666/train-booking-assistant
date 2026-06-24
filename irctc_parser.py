import re
from datetime import datetime


def extract_first(pattern, text):

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return ""


def normalize_date(date_string):

    try:

        return datetime.strptime(
            date_string,
            "%d-%b-%Y"
        ).strftime("%Y-%m-%d")

    except Exception:

        return date_string


def parse_irctc_email(
    subject,
    html
):

    booking = {}

    # --------------------------------
    # Subject Parsing
    # --------------------------------

    subject_pattern = (
        r"Train:\s*(\d+),\s*"
        r"(\d{2}-[A-Za-z]{3}-\d{4}),\s*"
        r"([^,]+),\s*"
        r"([A-Z]+)\s*-\s*([A-Z]+)"
    )

    subject_match = re.search(
        subject_pattern,
        subject
    )

    if subject_match:

        booking["train"] = subject_match.group(1)

        booking["date"] = normalize_date(
            subject_match.group(2)
        )

        booking["class"] = (
            subject_match.group(3)
        )

        booking["route"] = (
            f"{subject_match.group(4)}-"
            f"{subject_match.group(5)}"
        )

    # --------------------------------
    # PNR
    # --------------------------------

    booking["pnr"] = extract_first(
        r"PNR No\.\s*:</b></td>.*?<span>(.*?)</span>",
        html
    )

    # --------------------------------
    # Full Class Name
    # --------------------------------

    full_class = extract_first(
        r"Class\s*:\s*</b></td>.*?<span>(.*?)</span>",
        html
    )

    if full_class:
        booking["class"] = full_class

    # --------------------------------
    # Passenger Status
    # --------------------------------

    status_match = re.search(
        r"<td[^>]*>N/A</td>\s*"
        r"<td[^>]*>(.*?)</td>\s*"
        r"<td[^>]*>(.*?)</td>\s*"
        r"<td[^>]*>(.*?)</td>",
        html,
        re.IGNORECASE | re.DOTALL
    )

    if status_match:

        booking["status"] = (
            status_match.group(1)
            .replace("&nbsp;", "")
            .strip()
        )

        booking["coach"] = (
            status_match.group(2)
            .replace("&nbsp;", "")
            .strip()
        )

        booking["berth"] = (
            status_match.group(3)
            .replace("&nbsp;", "")
            .strip()
        )

    return booking


if __name__ == "__main__":

    sample_subject = (
        "Booking Confirmation on IRCTC, "
        "Train: 20653, "
        "30-Jul-2026, "
        "SL, "
        "SBC - BGM"
    )

    with open(
        "irctc_booking_email.html",
        "r",
        encoding="utf-8"
    ) as file:

        html = file.read()

    booking = parse_irctc_email(
        sample_subject,
        html
    )

    print("\nParsed Booking\n")

    for key, value in booking.items():
        print(f"{key}: {value}")