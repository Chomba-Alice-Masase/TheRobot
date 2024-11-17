from django.urls import path
# stream/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('video-feed', views.video_feed, name='video_feed'),  # For streaming
]
