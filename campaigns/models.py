from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class EmailGroup(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    first_name = models.CharField(max_length=255, null=True, blank=True)  # Add this line

    def __str__(self):
        return self.name

class EmailCampaign(models.Model):
    group = models.ForeignKey(EmailGroup, on_delete=models.CASCADE, related_name='campaigns')
    subject = models.CharField(max_length=255, help_text="Subject of the email")
    body = models.TextField(help_text="Body of the email")
    scheduled_time = models.DateTimeField(help_text="Time to send the emails")
    smtp_account = models.CharField(
        max_length=100,
        choices=[('gmail', 'Gmail'), ('outlook', 'Outlook')],
        help_text="SMTP account to use for sending emails"
    )
    sent = models.BooleanField(default=False, help_text="Whether the campaign has been sent")

    def __str__(self):
        return f"Campaign: {self.subject}"

class EmailLog(models.Model):
    email_campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE, related_name='logs')
    recipient = models.EmailField(help_text="Recipient email address")
    sent_at = models.DateTimeField(null=True, blank=True, help_text="Time when the email was sent")
    replied = models.BooleanField(default=False, help_text="Whether the recipient replied to the email")

    def __str__(self):
        return f"Email to {self.recipient} - {'Replied' if self.replied else 'No Reply'}"
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmailCampaign, EmailLog

@receiver(post_save, sender=EmailCampaign)
def create_logs_for_campaign(sender, instance, created, **kwargs):
    if created:
        # Extract recipients from the associated EmailGroup
        recipients = instance.group.emails
        for recipient in recipients:
            EmailLog.objects.create(email_campaign=instance, recipient=recipient)
