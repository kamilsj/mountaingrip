from django.urls import path
from . import views

urlpatterns = [
    path('', views.Inbox.as_view(), name='index'),
]