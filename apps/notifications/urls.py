from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotifView.as_view(), name='index'),
]