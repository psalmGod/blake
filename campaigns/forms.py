import json
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField
from .models import EmailGroup, EmailCampaign

class EmailGroupForm(forms.ModelForm):
    class Meta:
        model = EmailGroup
        fields = ['name', 'emails']
        widgets = {
            'emails': forms.Textarea(attrs={'placeholder': 'Enter emails as JSON (["email1@example.com", "email2@example.com"])'}),
        }

    def clean_emails(self):
        emails = self.cleaned_data['emails']
        try:
            email_list = emails
            if not isinstance(email_list, list):
                raise ValidationError("Emails should be a list of email addresses.")
            for email in email_list:
                if '@' not in email:
                    raise ValidationError(f"Invalid email address: {email}")
        except json.JSONDecodeError:
            raise ValidationError("Emails should be valid JSON.")
        return emails

class EmailCampaignForm(forms.ModelForm):
    group = ModelChoiceField(
        queryset=EmailGroup.objects.all(),
        empty_label="Select an email group",
        label="Email Group",
    )

    class Meta:
        model = EmailCampaign
        fields = ['group', 'subject', 'body', 'scheduled_time', 'smtp_account']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
from django import forms

class CSVUploadForm(forms.Form):
    file = forms.FileField(label="Upload CSV File", help_text="Upload a CSV file with the same format as the Twenty API.")


from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email Address", help_text="Enter your email address.")
    password = forms.CharField(widget=forms.PasswordInput, label="App Password", help_text="Enter your email app password.")

class SMTPConfigForm(forms.Form):
    email = forms.EmailField(label="Email Address", help_text="Your email address for SMTP (e.g., Gmail or Outlook).")
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="App Password",
        help_text="Your app password. Visit Google or Outlook to generate it."
    )
