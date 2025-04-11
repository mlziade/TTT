from django.urls import path
from .views import (
    HomeView,
    TextView,
)

app_name = 'text_through_tweet'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('text/', TextView.as_view(), name='text'),
]
