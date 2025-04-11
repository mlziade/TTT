from django.urls import path
from .views import (
    HomeView,
)

app_name = 'text_through_tweet'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
