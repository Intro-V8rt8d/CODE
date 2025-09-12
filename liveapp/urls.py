from django.urls import path
from .views import start_live, join_live, room, end_live, attendance

urlpatterns = [
    path("", start_live, name="start"),
    path("join/", join_live, name="join"),
    path("room/<str:room>/", room, name="room"),
    path("room/<str:room>/end/", end_live, name="end"),
    path("room/<str:room>/attendance/", attendance, name="attendance"),
]
