from django.urls import path
from .views import CreateOrderView

urlpatterns = [
    path('create_order/', CreateOrderView.as_view()),
]