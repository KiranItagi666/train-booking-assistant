import os
import json
import base64
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

print("This will open a browser window to authorize Gmail access.")
print("After approval, it will save token.json and print the GitHub secret values.")

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials.json",
    SCOPES,
)

creds = flow.run_local_server(port=0)

with open("token.json", "w", encoding="utf-8") as f:
    f.write(creds.to_json())

with open("token.json", "r", encoding="utf-8") as f:
    token_data = json.load(f)

print("\nToken saved to token.json")
print("\nGitHub Secret: GOOGLE_TOKEN")
print(base64.b64encode(json.dumps(token_data).encode("utf-8")).decode("utf-8"))
print("\nGitHub Secret: GOOGLE_CREDENTIALS")
print(base64.b64encode(open("credentials.json", "rb").read()).decode("utf-8"))
