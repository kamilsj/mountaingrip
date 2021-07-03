from django.urls import path
from . import views

app_name = 'inbox'
urlpatterns = [
    path('', views.Inbox.as_view(), name='index'),
    path('sent/', views.SentView.as_view(), name='sent'),
    path('message/<int:id>/', views.MessageView.as_view(), name='message')
]