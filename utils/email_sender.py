# utils/email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from data.config import GMAIL_ADDRESS, GMAIL_PASSWORD
import traceback

def send_email(to_email, subject, body):
    print(f"Attempting to send email to {to_email}")
    print(f"Subject: {subject}")
    print(f"Body: {body[:100]}...") # Print first 100 characters of the body

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = GMAIL_ADDRESS
    message['To'] = to_email
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    # Create SMTP session
    try:
        print("Connecting to SMTP server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            print("Connected. Starting TLS...")
            server.starttls()
            print(f"Logging in with email: {GMAIL_ADDRESS}")
            server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
            text = message.as_string()
            print("Sending email...")
            server.sendmail(GMAIL_ADDRESS, to_email, text)
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        return False

# Test function
def test_email_sending():
    print("Testing email functionality...")
    result = send_email(GMAIL_ADDRESS, "Test Subject", "This is a test email body.")
    if result:
        print("Test email sent successfully.")
    else:
        print("Failed to send test email.")

if __name__ == "__main__":
    test_email_sending()