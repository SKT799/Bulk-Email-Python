# Bulk Email Sender (Python)

This repo contains a simple bulk email sender script implemented in `Code.py`. The script supports plain-text and optional HTML messages, attachments, configurable SMTP settings (Gmail, Outlook, Yahoo examples), and a small delay between sends to reduce rate-limiting.

> Important: Do NOT store real passwords directly in the script. Use environment variables, a .env file with `python-dotenv`, or a secrets manager. See the Security section below.

## Features

- Send plain-text or HTML emails
- Attach a single file (optional)
- Support for common SMTP providers (Gmail, Outlook/Hotmail, Yahoo)
- Delay between sends to avoid rate limiting
- Connection/test helpers to validate SMTP settings and App Password format
- Interactive confirmation before sending

## Files

- `Code.py` — Main script. Configure SMTP, sender credentials, recipients, subject, and body at the top of the file. Run as a script to test and send emails.
- `README_Email_Sender.md` — This file (documentation for the email sender)

## Requirements

- Python 3.8+
- Packages used (standard library only): `smtplib`, `email`, `time`, `os`

Optional helper packages (recommended for secure configuration):

- `python-dotenv` — load credentials from a `.env` file

Install optional package with:

```bash
pip install python-dotenv
```

## Configuration

Open `Code.py` and update the configuration block near the top:

- `SENDER_EMAIL` — the email address you'll send from
- `SENDER_PASSWORD` — an App Password (for Gmail) or account password (not recommended)
- `SMTP_SERVER` and `SMTP_PORT` — server and port for your provider
- `EMAIL_LIST` — list of recipient email addresses
- `EMAIL_SUBJECT`, `EMAIL_BODY`, `EMAIL_BODY_HTML` — message content
- `USE_HTML` — set to `True` to include the HTML body
- `ATTACHMENT_PATH` — path to a file to attach, or empty string
- `DELAY_BETWEEN_EMAILS` — number of seconds to wait between sends

### Gmail-specific notes

- If you use Gmail, enable 2-step verification and create an App Password. Use the 16-character App Password as `SENDER_PASSWORD`.
- App Passwords are shown once when created. Store them securely.

## Secure configuration examples

Preferred: set credentials as environment variables instead of hardcoding.

Windows (cmd.exe):

```cmd
setx SENDER_EMAIL "your.email@example.com"
setx SENDER_PASSWORD "your_16_char_app_password"
```

Then, in Python, read them with `os.environ.get('SENDER_EMAIL')` and `os.environ.get('SENDER_PASSWORD')`.

Optional: use a `.env` file and `python-dotenv`:

```
# .env
SENDER_EMAIL=your.email@example.com
SENDER_PASSWORD=your_16_char_app_password
```

Load in your script:

```python
from dotenv import load_dotenv
load_dotenv()
import os
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
```

## How to run

1. Review and update the top configuration section in `Code.py`.
2. (Optional) Test SMTP connection and login using the script's built-in tests:

```cmd
cd /d "c:\Users\satya\OneDrive\Desktop\GIT_PROJECTS"
python Code.py
```

The script will run several checks:
- App password format check
- Attempts to connect to common SMTP configurations
- Attempts to login (if credentials are set)

After checks, the script will prompt you to confirm before actually sending emails.

## Example: Use environment variables in `Code.py`

Replace the hardcoded values with:

```python
import os
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
```

## Attachments

Set `ATTACHMENT_PATH` to a valid file path (e.g., `"C:\path\to\file.pdf"`). The script checks file existence before attaching.

## Rate limiting and delays

Use `DELAY_BETWEEN_EMAILS` to add a pause between sends. For large campaigns, consider batching and respecting provider limits.

## Security & best practices

- Never commit real credentials to source control.
- Use App Passwords for Gmail and rotate them periodically.
- For large-scale sending, use a dedicated transactional email service (SendGrid, Amazon SES, Mailgun) that handles deliverability and rate limits.
- Consider adding logging and exponential backoff for transient SMTP errors.
- Validate recipient addresses before sending.

## Troubleshooting

- Authentication errors: confirm App Password, 2FA enabled, and correct sender email.
- Connection errors: verify `SMTP_SERVER` and `SMTP_PORT` are correct and outbound SMTP is allowed on your network.
- Attachment issues: ensure the file path is correct and the script has read permissions.

## Suggested improvements

- Move configuration to a separate `config.py` or use environment variables and `python-dotenv`.
- Add logging with rotating file handlers.
- Add retry/backoff logic on transient SMTP errors.
- Add support for CSV input of recipients and templated personalization.
- Add tests for the connection helpers and message-building functionality.

## License & Attribution

Add a `LICENSE` file if you want to make the project public with explicit terms (MIT/Apache-2.0/etc.).

---

If you'd like, I can also:
- Commit and push this README for you (I can do that here as I pushed the previous README).
- Add a `.env.example` or `requirements.txt`.
- Refactor `Code.py` to load credentials from environment variables and add unit tests for the helper functions.

Which of the above would you like next?
