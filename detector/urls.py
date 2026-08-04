from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('image/', views.image_page, name='image'),
    path('video/', views.video_page, name='video'),
    path('live/', views.live_page, name='live'),

    path('detect-image/', views.detect_image, name='detect_image'),
    path('detect-video/', views.detect_video, name='detect_video'),

    path('run-live/', views.run_live, name='run_live'),
    path("send-email/", views.send_email_view, name="send_email"),
]