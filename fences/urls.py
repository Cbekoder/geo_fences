from django.urls import path
from .views import LocationCheckView

urlpatterns = [
    path("location-check", LocationCheckView.as_view(), name="location-check"),
]
