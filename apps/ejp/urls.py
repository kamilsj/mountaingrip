from django.urls import path
from . import views

urlpatterns = [
    path('', views.EJPView.as_view(), name='index'),
    path('predictions/', views.Predictions.as_view(), name='predictions'),
    path('plusminus/', views.PlusMinus.as_view(), name='plusminus'),
]