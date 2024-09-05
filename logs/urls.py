from django.urls import path
from .views import get_logs, get_events

urlpatterns = [
    path('get-logs/', get_logs, name='get_logs'),
    path('get-events/', get_events, name='get_events'),
]
