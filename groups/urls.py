from django.urls import path
from . import views

urlpatterns = [
    path('', views.GroupExplore.as_view(), name='index'),
    path('<int:id>/', views.GroupView.as_view(), name='group_view'),
    path('create/', views.GroupCreate.as_view(), name='group_create'),
]