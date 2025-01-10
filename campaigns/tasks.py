from celery import shared_task
from time import sleep
from .models import EmailCampaign, EmailLog
from .utils import send_email
from django.utils.timezone import now

@shared_task
def send_campaign_emails(campaign_id, sender_email, sender_password, delay=5):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Task started with campaign_id={campaign_id}, sender_email={sender_email}")
    """
    Send emails in a campaign with a delay between each email.

    :param campaign_id: ID of the EmailCampaign
    :param sender_email: Sender's email address
    :param sender_password: Sender's email password
    :param delay: Delay in seconds between each email (default: 5 seconds)
    """
    campaign = EmailCampaign.objects.get(id=campaign_id)
    logs = campaign.logs.filter(sent_at__isnull=True)


    for log in logs:
        success = send_email(
            smtp_account=campaign.smtp_account,
            sender_email=sender_email,
            sender_password=sender_password,
            recipient=log.recipient,
            subject=campaign.subject,
            body=campaign.body,
        )
        if success:
            log.sent_at = now()
            log.save()
            sleep(delay)  # Add delay between sending emails
@shared_task
def send_campaign_emails_with_reply_check(campaign_id, sender_email, sender_password, delay=5):
    campaign = EmailCampaign.objects.get(id=campaign_id)
    logs = campaign.logs.filter(sent_at__isnull=True)

    for log in logs:
        # Check for replies before sending
        replied_emails = check_replies(
            smtp_account=campaign.smtp_account,
            email_address=sender_email,
            email_password=sender_password,
            campaign_subject=campaign.subject,
        )

        if log.recipient in replied_emails:
            log.replied = True
            log.save()
            continue  # Skip sending to recipients who replied

        # Send the email
        success = send_email(
            smtp_account=campaign.smtp_account,
            sender_email=sender_email,
            sender_password=sender_password,
            recipient=log.recipient,
            subject=campaign.subject,
            body=campaign.body,
        )
        if success:
            log.sent_at = now()
            log.save()
            sleep(delay)

@shared_task
def test_task(arg1, arg2):
    print(f"Test Task: arg1={arg1}, arg2={arg2}")
    return f"Received {arg1} and {arg2}"
