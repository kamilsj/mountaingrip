from django.urls import path
from . import views

urlpatterns = [
    path('', views.GroupExplore.as_view(), name='index'),
    path('<int:id>/', views.GroupView.as_view(), name='group_view'),
    path('<int:gid>/<int:tid>/', views.ThreadView.as_view(), name='thread_view'),
    path('create/', views.GroupCreate.as_view(), name='group_create'),
]