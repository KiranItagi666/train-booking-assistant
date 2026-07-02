import unittest
from unittest.mock import Mock, patch

from google.auth.exceptions import RefreshError

from gmail_reader import GmailAuthError, get_gmail_service


class GmailReaderTests(unittest.TestCase):
    @patch("gmail_reader.os.remove")
    @patch("gmail_reader.Credentials.from_authorized_user_file")
    @patch("gmail_reader.os.path.exists", return_value=True)
    def test_refresh_error_is_wrapped_as_gmail_auth_error(self, mock_exists, mock_from_file, mock_remove):
        creds = Mock()
        creds.valid = False
        creds.expired = True
        creds.refresh_token = "refresh-token"
        creds.refresh.side_effect = RefreshError("invalid_grant")
        mock_from_file.return_value = creds

        with self.assertRaises(GmailAuthError):
            get_gmail_service()

        mock_remove.assert_called_once_with("token.json")


if __name__ == "__main__":
    unittest.main()
