from django.urls import path
from . import views

app_name =  'inbox'
urlpatterns = [
    path('', views.Inbox.as_view(), name='index'),
]