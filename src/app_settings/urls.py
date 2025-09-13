from django.urls import path
from .views import AppSettingsView, GetlogoView

app_name = 'settings'

urlpatterns = [
    path('app-settings/', AppSettingsView.as_view(), name='app-settings'),
    path('getlogo/', GetlogoView.as_view(), name='getlogo'),
] 