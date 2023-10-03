from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('robots/', include('robots.urls')),
    path('orders/', include('orders.urls')),
    path('admin/', admin.site.urls),
]
