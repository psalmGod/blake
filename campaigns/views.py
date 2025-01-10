import logging
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmailGroupForm, EmailCampaignForm
from .models import EmailCampaign, EmailGroup, EmailLog
from .tasks import send_campaign_emails
from .decorators import login_required

# Logger setup
logger = logging.getLogger(__name__)


# Home View
@login_required
def home(request):
    return render(request, 'campaigns/home.html')

# Email Groups View

def email_groups(request):
    if request.method == 'POST':
        form = EmailGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('email_groups')
    else:
        form = EmailGroupForm()

    groups = EmailGroup.objects.all()
    return render(request, 'campaigns/email_groups.html', {'form': form, 'groups': groups})

# Campaign List and Create View
def campaigns(request):
    if request.method == 'POST':
        form = EmailCampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campaigns')
    else:
        form = EmailCampaignForm()

    campaigns = EmailCampaign.objects.all()
    return render(request, 'campaigns/campaigns.html', {'form': form, 'campaigns': campaigns})

# Send Campaign View
from .tasks import send_campaign_emails
from django.shortcuts import redirect
from django.contrib import messages
from .decorators import login_required

from .tasks import send_campaign_emails


def send_campaign(request, campaign_id):
    if request.method == "POST":
        smtp_email = request.session.get("smtp_email")
        smtp_password = request.session.get("smtp_password")

        if not smtp_email or not smtp_password:
            messages.error(request, "SMTP settings are not configured. Please configure them first.")
            return redirect("smtp_config")

        send_campaign_emails(campaign_id, smtp_email, smtp_password, 15)
        messages.success(request, "Campaign sending started.")
        return redirect("campaigns")


from .models import EmailCampaign, EmailLog 

def create_campaign(request):
    if request.method == 'POST':
        form = EmailCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save()

            # Directly access the emails field (already a Python list)
            email_list = campaign.group.emails
            for email in email_list:
                EmailLog.objects.create(email_campaign=campaign, recipient=email)

            return redirect('campaigns')
    else:
        form = EmailCampaignForm()

    return render(request, 'campaigns/create_campaign.html', {'form': form})

from django.shortcuts import redirect
from django.contrib import messages
from .models import EmailGroup
from .utils import TwentyAPI

def fetch_twenty_data(request):
    """
    Fetch data from Twenty CRM API and save it to EmailGroup.
    """
    try:
        # Fetch emails from Twenty
        email_list = TwentyAPI.get_people()

        # Save the emails to a new EmailGroup
        group = EmailGroup.objects.create(
            name="Imported from Twenty",
            emails=email_list
        )

        messages.success(request, f"Successfully imported {len(email_list)} emails.")
    except Exception as e:
        messages.error(request, f"Error fetching data from Twenty: {str(e)}")

    return redirect("email_groups")

import csv
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CSVUploadForm
from .models import EmailGroup

def upload_csv_emails(request):
    """
    View to handle CSV file uploads and create an EmailGroup from the uploaded data.
    """
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded_file = request.FILES["file"]
                email_list = []

                # Process the CSV file
                csv_file = csv.DictReader(uploaded_file.read().decode("utf-8").splitlines())
                for row in csv_file:
                    primary_email = row.get("Emails PrimaryEmail")
                    if primary_email and "@" in primary_email:
                        email_list.append(primary_email)

                # Save to EmailGroup
                group = EmailGroup.objects.create(
                    name="Uploaded from CSV",
                    emails=email_list
                )
                messages.success(request, f"Successfully uploaded {len(email_list)} emails.")
                return redirect("email_groups")
            except Exception as e:
                messages.error(request, f"Error processing CSV file: {str(e)}")
                return redirect("email_groups")
    else:
        form = CSVUploadForm()

    return render(request, "campaigns/upload_csv.html", {"form": form})

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib import messages

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful. Welcome!")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "campaigns/signup.html", {"form": form})

from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    """
    Handles user login using Django's built-in AuthenticationForm.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return render(request, 'campaigns/home.html')  # Redirect to the homepage
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "campaigns/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


from .forms import SMTPConfigForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def smtp_config(request):
    """
    View to configure SMTP settings for sending emails.
    """
    if request.method == "POST":
        form = SMTPConfigForm(request.POST)
        if form.is_valid():
            # Save SMTP settings in the session
            request.session["smtp_email"] = form.cleaned_data["email"]
            request.session["smtp_password"] = form.cleaned_data["password"]

            messages.success(request, "SMTP settings configured successfully.")
            return redirect("email_groups")
    else:
        form = SMTPConfigForm()

    return render(request, "campaigns/smtp_config.html", {"form": form})

