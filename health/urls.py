from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('import/', views.ImportActivities.as_view(),  name='import_activities'),
    #path('activities/')
]