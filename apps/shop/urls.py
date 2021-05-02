from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('purchases/', views.Purchases.as_view(), name='purchases'),
]