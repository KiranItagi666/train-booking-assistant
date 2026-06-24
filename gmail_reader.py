from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import base64
import os

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


def get_gmail_service():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

        with open("token.json", "w") as token:
            token.write(
                creds.to_json()
            )

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


def get_irctc_emails(
    service,
    max_results=20
):

    results = service.users().messages().list(
        userId="me",
        q="from:ticketadmin@irctc.co.in newer_than:365d",
        maxResults=max_results
    ).execute()

    return results.get(
        "messages",
        []
    )


def get_email_details(
    service,
    message_id
):

    return service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()


def get_subject(email):

    for header in email["payload"]["headers"]:

        if header["name"] == "Subject":
            return header["value"]

    return "No Subject"


def decode_email_body(email):

    try:

        if "parts" in email["payload"]:

            for part in email["payload"]["parts"]:

                if part["mimeType"] in [
                    "text/plain",
                    "text/html"
                ]:

                    data = part["body"].get(
                        "data"
                    )

                    if not data:
                        continue

                    return base64.urlsafe_b64decode(
                        data
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

        data = email["payload"]["body"].get(
            "data"
        )

        if data:

            return base64.urlsafe_b64decode(
                data
            ).decode(
                "utf-8",
                errors="ignore"
            )

    except Exception as e:

        return f"ERROR: {e}"

    return ""


def save_email_html(
    content,
    filename="irctc_booking_email.html"
):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)


def main():

    service = get_gmail_service()

    messages = get_irctc_emails(
        service
    )

    print(
        f"\nFound {len(messages)} IRCTC emails\n"
    )

    for index, msg in enumerate(
        messages,
        start=1
    ):

        email = get_email_details(
            service,
            msg["id"]
        )

        subject = get_subject(
            email
        )

        body = decode_email_body(
            email
        )

        print("=" * 80)
        print(f"EMAIL {index}")
        print("=" * 80)

        print("SUBJECT:")
        print(subject)

        print()
        print("BODY PREVIEW:")
        print(body[:1000])

        print()

        if (
            "Booking Confirmation on IRCTC"
            in subject
        ):

            save_email_html(
                body
            )

            print(
                "Saved booking email to "
                "irctc_booking_email.html"
            )

            break


if __name__ == "__main__":
    main()