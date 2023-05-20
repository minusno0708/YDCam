from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("video_feed", views.video_feed_view(), name="video_feed"),
]