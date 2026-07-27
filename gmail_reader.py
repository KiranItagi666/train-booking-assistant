from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import base64
import os

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


class GmailAuthError(RuntimeError):
    """Raised when Gmail credentials are unavailable or invalid."""


def get_gmail_service():

    if not os.path.exists("credentials.json"):
        raise GmailAuthError(
            "\n"
            "credentials.json not found.\n\n"
            "Fix:\n"
            "1. Download OAuth Desktop Client credentials from Google Cloud.\n"
            "2. Save it as credentials.json.\n"
            "3. Update the GOOGLE_CREDENTIALS GitHub Secret."
        )

    if not os.path.exists("token.json"):
        raise GmailAuthError(
            "\n"
            "token.json not found.\n\n"
            "Fix:\n"
            "1. Run:\n"
            "   python generate_gmail_token.py\n"
            "2. Sign in to Google.\n"
            "3. Update the GOOGLE_TOKEN GitHub Secret."
        )

    creds = None

    try:

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    except ValueError as exc:

        if os.path.exists("token.json"):
            os.remove("token.json")

        raise GmailAuthError(
            "\n"
            "token.json is corrupted or invalid.\n\n"
            "Fix:\n"
            "1. Delete token.json.\n"
            "2. Run generate_gmail_token.py.\n"
            "3. Update GOOGLE_TOKEN GitHub Secret.\n\n"
            f"Original Error:\n{exc}"
        ) from exc

    if not creds.valid:

        if creds.expired and creds.refresh_token:

            try:

                creds.refresh(Request())

            except RefreshError as exc:

                error = str(exc).lower()

                if os.path.exists("token.json"):
                    os.remove("token.json")

                if "deleted_client" in error:

                    raise GmailAuthError(
                        "\n"
                        "Google OAuth client has been deleted.\n\n"
                        "Fix:\n"
                        "1. Create a new OAuth Desktop Client.\n"
                        "2. Download credentials.json.\n"
                        "3. Replace credentials.json.\n"
                        "4. Delete token.json.\n"
                        "5. Run generate_gmail_token.py.\n"
                        "6. Update GOOGLE_CREDENTIALS.\n"
                        "7. Update GOOGLE_TOKEN."
                    ) from exc

                elif "invalid_grant" in error:

                    raise GmailAuthError(
                        "\n"
                        "Google refresh token is no longer valid.\n\n"
                        "Fix:\n"
                        "1. Delete token.json.\n"
                        "2. Run generate_gmail_token.py.\n"
                        "3. Sign in again.\n"
                        "4. Update GOOGLE_TOKEN GitHub Secret."
                    ) from exc

                elif "invalid_client" in error:

                    raise GmailAuthError(
                        "\n"
                        "credentials.json does not match the OAuth client.\n\n"
                        "Fix:\n"
                        "Download the correct credentials.json from the same "
                        "Google Cloud project that created the token."
                    ) from exc

                else:

                    raise GmailAuthError(
                        "\n"
                        "Google OAuth token refresh failed.\n\n"
                        f"{exc}"
                    ) from exc

            except Exception as exc:

                if os.path.exists("token.json"):
                    os.remove("token.json")

                raise GmailAuthError(
                    "\n"
                    "Unexpected Gmail authentication failure.\n\n"
                    f"{exc}"
                ) from exc

            with open("token.json", "w") as token:
                token.write(
                    creds.to_json()
                )

        else:

            if os.path.exists("token.json"):
                os.remove("token.json")

            raise GmailAuthError(
                "\n"
                "No valid Gmail credentials available.\n\n"
                "Run:\n"
                "python generate_gmail_token.py"
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

                    data = part["body"].get("data")

                    if not data:
                        continue

                    return base64.urlsafe_b64decode(
                        data
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

        data = email["payload"]["body"].get("data")

        if data:

            return base64.urlsafe_b64decode(
                data
            ).decode(
                "utf-8",
                errors="ignore"
            )

    except Exception as exc:

        return f"ERROR: {exc}"

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

    try:

        service = get_gmail_service()

    except GmailAuthError as exc:

        print("=" * 80)
        print("GMAIL AUTHENTICATION ERROR")
        print("=" * 80)
        print(exc)
        print("=" * 80)
        return

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