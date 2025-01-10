from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EmailGroup, EmailCampaign, EmailLog

@admin.register(EmailGroup)
class EmailGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'group', 'scheduled_time', 'smtp_account', 'sent')
    search_fields = ('subject', 'group__name')
    list_filter = ('scheduled_time', 'smtp_account', 'sent')

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('email_campaign', 'recipient', 'sent_at', 'replied')
    search_fields = ('recipient', 'email_campaign__subject')
    list_filter = ('replied', 'sent_at')
