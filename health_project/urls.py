# project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('health.urls')),  # Replace 'yourapp' with the name of your app
]
