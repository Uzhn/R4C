from django.contrib import admin
from django.urls import path
from .views import RobotAPIView

urlpatterns = [
    path('create_robot/', RobotAPIView.as_view()),
]
