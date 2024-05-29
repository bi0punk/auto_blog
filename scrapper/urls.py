from django.urls import path
from .views import check_url

urlpatterns = [
    path('', check_url, name='check_url'),
]
