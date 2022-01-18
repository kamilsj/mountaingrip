from django.urls import path
from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.GroupExplore.as_view(), name='index'),
    path('<int:id>/', views.GroupView.as_view(), name='group_view'),
    path('<int:gid>/<int:tid>/', views.ThreadView.as_view(), name='thread_view'),
    path('<int:id>/settings/', views.GroupViewSettings.as_view(), name='group_view_settings'),
    path('create/', views.GroupCreate.as_view(), name='group_create'),
]