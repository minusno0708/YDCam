from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path

#from config import settings
from . import views

urlpatterns = [
    path('stream', views.IndexView.as_view()),
    path('video_feed', views.video_feed_view(), name="video_feed"),
]
urlpatterns += staticfiles_urlpatterns()