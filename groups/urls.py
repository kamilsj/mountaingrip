from django.urls import path
from . import views

urlpatterns = [
    path('', views.Group.as_view(), name='index'),
]