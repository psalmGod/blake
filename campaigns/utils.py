import smtplib
from email.mime.text import MIMEText

def send_email(smtp_account, sender_email, sender_password, recipient, subject, body):
    smtp_host = "smtp.gmail.com" if smtp_account == "gmail" else "smtp.office365.com"
    smtp_port = 587

    # Create the email
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
import imaplib
import email

def check_replies(smtp_account, email_address, email_password, campaign_subject):
    """
    Check the inbox for replies to a specific campaign.

    :param smtp_account: SMTP account (e.g., "gmail" or "outlook")
    :param email_address: Email address to check
    :param email_password: Password for the email account
    :param campaign_subject: Subject of the campaign to match replies
    :return: List of email addresses that replied
    """
    imap_host = "imap.gmail.com" if smtp_account == "gmail" else "outlook.office365.com"
    replied_emails = []

    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(email_address, email_password)
        mail.select("inbox")

        # Search for emails that contain the campaign subject
        status, messages = mail.search(None, f'SUBJECT "{campaign_subject}"')
        email_ids = messages[0].split()

        for email_id in email_ids:
            # Fetch the email
            status, data = mail.fetch(email_id, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Extract the sender's email
            from_email = msg.get("From")
            replied_emails.append(from_email)

        mail.logout()
    except Exception as e:
        print(f"Error checking replies: {e}")

    return replied_emails

import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TwentyAPI:
    @staticmethod
    def get_people():
        headers = {
            "Authorization": f"Bearer {settings.TWENTY_API_KEY}"
        }
        response = requests.get(f"{settings.TWENTY_API_BASE_URL}/people", headers=headers)

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Response Data: {data}")  # Log the response for debugging

            # Extract emails from the people list
            people = data.get("data", {}).get("people", [])
            email_list = [
                person["emails"]["primaryEmail"]
                for person in people
                if person.get("emails") and person["emails"].get("primaryEmail")
            ]
            return email_list
        else:
            raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")

