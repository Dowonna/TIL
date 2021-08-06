from django.urls import path
from . import views

urlpatterns = [
    path('ad/', views.ad),  # /another/ad/
    path('reply/', views.reply)  # /another/reply
]