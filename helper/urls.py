from django.urls import path
from helper.apps import HelperConfig
from helper.views import MailingAPIView

app_name = HelperConfig.name

urlpatterns = [
    path('notify/', MailingAPIView.as_view(), name='create'),
]
