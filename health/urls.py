from django.urls import path
from . import views

app_name = 'health'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('import/', views.ImportActivities.as_view(),  name='import_activities'),
    path('analytics/', views.Analytics.as_view(), name='analytics'),
    path('summary/', views.Summary.as_view(), name='summary'),
]