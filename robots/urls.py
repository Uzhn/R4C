from django.contrib import admin
from django.urls import path
from .views import RobotAPIView, RobotExcelView

urlpatterns = [
    path('create_robot/', RobotAPIView.as_view()),
    path('download_robot_list/', RobotExcelView.as_view())
]
