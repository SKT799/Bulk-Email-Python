import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
import os

# ================ CONFIGURATION ================
# Email account credentials
SENDER_EMAIL = "satyamkumar100me100@gmail.com"  # Replace with your email
SENDER_PASSWORD = "Your_Gmail_App_Password"   # Removed spaces and add here

# SMTP Server Settings (Choose based on your email provider)
# Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Outlook/Hotmail (uncomment if using)
# SMTP_SERVER = "smtp-mail.outlook.com"
# SMTP_PORT = 587

# Yahoo (uncomment if using)
# SMTP_SERVER = "smtp.mail.yahoo.com"
# SMTP_PORT = 587

# Email list - Add recipient emails here
EMAIL_LIST = [
    "satyamkumar100me100@gmail.com",
    "21cs2019@rgipt.ac.in"
]

# Email content
EMAIL_SUBJECT = "Your Subject Here"
EMAIL_BODY = """
Dear Recipient,

This is the body of your email. You can write multiple lines here.

You can format this however you want.

Best regards,
Your Name
"""

# Optional: HTML body (uncomment to use HTML instead of plain text)
EMAIL_BODY_HTML = """
<html>
  <body>
    <h2>Hello!</h2>
    <p>This is an <b>HTML</b> email.</p>
    <p>You can include <a href="https://example.com">links</a> and formatting.</p>
  </body>
</html>
"""
USE_HTML = False  # Set to True to use HTML body

# Optional: Attachment file path (leave empty if no attachment)
ATTACHMENT_PATH = ""  # e.g., "document.pdf"

# Delay between emails (in seconds) to avoid rate limiting
DELAY_BETWEEN_EMAILS = 2

# ================ EMAIL SENDING FUNCTION ================

def send_email(recipient_email, subject, body, html_body=None, attachment_path=None):
    """
    Send an email to a single recipient
    
    Args:
        recipient_email: Email address of the recipient
        subject: Subject of the email
        body: Plain text body of the email
        html_body: Optional HTML body
        attachment_path: Optional path to attachment file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add plain text part
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML part if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Add attachment if provided
        if attachment_path and os.path.isfile(attachment_path):
            with open(attachment_path, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
        
        # Connect to server and send email
        print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(1)  # Enable debug output
            print("Starting TLS...")
            server.starttls()  # Enable encryption
            print("Logging in...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Sending message...")
            server.send_message(msg)
            print("Message sent successfully!")
        
        return True
    
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication failed for {recipient_email}:")
        print("  - Make sure you're using an App Password, not your regular Gmail password")
        print("  - Enable 2-factor authentication and generate an App Password")
        print(f"  - Error details: {str(e)}")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP error sending email to {recipient_email}: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error sending email to {recipient_email}: {str(e)}")
        return False

def send_bulk_emails():
    """
    Send emails to all recipients in the EMAIL_LIST
    """
    successful = 0
    failed = 0
    failed_recipients = []
    
    print(f"Starting to send emails to {len(EMAIL_LIST)} recipients...")
    print("-" * 50)
    
    for i, email in enumerate(EMAIL_LIST, 1):
        print(f"[{i}/{len(EMAIL_LIST)}] Sending to: {email}")
        
        # Determine which body to use
        body_to_send = EMAIL_BODY
        html_to_send = EMAIL_BODY_HTML if USE_HTML else None
        
        # Send the email
        if send_email(
            recipient_email=email,
            subject=EMAIL_SUBJECT,
            body=body_to_send,
            html_body=html_to_send,
            attachment_path=ATTACHMENT_PATH if ATTACHMENT_PATH else None
        ):
            successful += 1
            print(f"    ✓ Successfully sent")
        else:
            failed += 1
            failed_recipients.append(email)
            print(f"    ✗ Failed to send")
        
        # Add delay between emails (except for the last one)
        if i < len(EMAIL_LIST):
            print(f"    Waiting {DELAY_BETWEEN_EMAILS} seconds...")
            time.sleep(DELAY_BETWEEN_EMAILS)
    
    # Print summary
    print("-" * 50)
    print("\nSUMMARY:")
    print(f"Total emails: {len(EMAIL_LIST)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if failed_recipients:
        print("\nFailed recipients:")
        for email in failed_recipients:
            print(f"  - {email}")
    
    return successful, failed

def validate_configuration():
    """
    Check if the configuration is properly set
    """
    errors = []
    
    if SENDER_EMAIL == "your_email@gmail.com":
        errors.append("Please set your SENDER_EMAIL")
    
    if SENDER_PASSWORD == "your_app_password_here" or SENDER_PASSWORD == "Jh@dfjhj489j":
        errors.append("Please set your SENDER_PASSWORD (use App Password for Gmail)")
    
    if not EMAIL_LIST:
        errors.append("EMAIL_LIST is empty")
    
    if not EMAIL_SUBJECT:
        errors.append("EMAIL_SUBJECT is empty")
    
    if not EMAIL_BODY and not (USE_HTML and EMAIL_BODY_HTML):
        errors.append("Email body is empty")
    
    if errors:
        print("Configuration errors found:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease fix these issues before running the script.")
        print("\nFor Gmail users:")
        print("1. Enable 2-factor authentication")
        print("2. Generate an App Password: https://support.google.com/accounts/answer/185833")
        print("3. Use the App Password instead of your regular password")
        return False
    
    return True

# Alternative: Add a test function with minimal authentication
def test_email_connection():
    """
    Test email connection with minimal setup
    """
    try:
        print("Testing email connection...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(1)
            server.starttls()
            
            # Try without login first (for testing connection)
            print("Connection successful!")
            print("Now testing login...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Login successful!")
            
        return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False

def check_app_password_format():
    """
    Check if the App Password format looks correct
    """
    if len(SENDER_PASSWORD) == 16 and SENDER_PASSWORD.isalnum():
        print("✓ App Password format looks correct (16 characters, alphanumeric)")
        return True
    else:
        print("✗ App Password format may be incorrect")
        print(f"  Current length: {len(SENDER_PASSWORD)} (should be 16)")
        print(f"  Contains only letters/numbers: {SENDER_PASSWORD.isalnum()}")
        print("  App Passwords should be 16 characters with no spaces or special characters")
        return False

def test_different_smtp_settings():
    """
    Test different SMTP configurations
    """
    print("Testing different SMTP configurations...")
    
    configs = [
        ("smtp.gmail.com", 587, "TLS"),
        ("smtp.gmail.com", 465, "SSL"),
        ("smtp.gmail.com", 25, "Plain")
    ]
    
    for server, port, method in configs:
        try:
            print(f"\nTrying {server}:{port} ({method})...")
            with smtplib.SMTP(server, port) as smtp_server:
                if port == 587:
                    smtp_server.starttls()
                elif port == 465:
                    smtp_server = smtplib.SMTP_SSL(server, port)
                
                print(f"✓ Connection to {server}:{port} successful")
                return server, port
        except Exception as e:
            print(f"✗ Failed {server}:{port}: {e}")
    
    return None, None

# ================ MAIN EXECUTION ================

if __name__ == "__main__":
    print("Email Sender Script")
    print("=" * 50)
    
    # Check App Password format
    print("Step 1: Checking App Password format...")
    check_app_password_format()
    print()
    
    # Test different SMTP settings
    print("Step 2: Testing SMTP configurations...")
    working_server, working_port = test_different_smtp_settings()
    if working_server:
        print(f"\n✓ Found working configuration: {working_server}:{working_port}")
        # Update global variables if different from current
        if working_server != SMTP_SERVER or working_port != SMTP_PORT:
            print("Updating SMTP settings...")
            SMTP_SERVER = working_server
            SMTP_PORT = working_port
    print()
    
    # Test connection with current settings
    print("Step 3: Testing email connection with authentication...")
    if not test_email_connection():
        print("\n❌ Connection test failed. Please check:")
        print("1. Your App Password is correct")
        print("2. 2-factor authentication is enabled on your Gmail account")
        print("3. You generated the App Password from the correct Google Account settings")
        print("4. The App Password hasn't been revoked")
        exit(1)
    
    print("\n✅ All tests passed!")
    
    # Validate configuration
    if not validate_configuration():
        exit(1)
    
    # Confirm before sending
    print(f"\nReady to send {len(EMAIL_LIST)} email(s)")
    print(f"From: {SENDER_EMAIL}")
    print(f"Subject: {EMAIL_SUBJECT}")
    
    if ATTACHMENT_PATH:
        print(f"Attachment: {ATTACHMENT_PATH}")
    
    response = input("\nDo you want to proceed? (yes/no): ").strip().lower()
    
    if response == 'yes':
        print("\nStarting email campaign...")
        successful, failed = send_bulk_emails()
        print(f"\nProcess completed! {successful} email(s) sent successfully.")
    else:
        print("Email sending cancelled.")
