from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('smtp-config/', views.smtp_config, name='smtp_config'),
    path('groups/', views.email_groups, name='email_groups'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('campaigns/create/', views.create_campaign, name='create_campaign'),
    path('campaigns/send/<int:campaign_id>/', views.send_campaign, name='send_campaign'),
    path('fetch-twenty-data/', views.fetch_twenty_data, name='fetch_twenty_data'),
    path('upload-csv/', views.upload_csv_emails, name='upload_csv_emails'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('email-groups/', views.email_groups, name='email_groups'),
    path('campaigns/', views.campaigns, name='campaigns'),
]

if settings.DEBUG:  # Only include Debug Toolbar in debug mode
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]