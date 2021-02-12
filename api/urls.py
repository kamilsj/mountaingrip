from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('graph/', views.ChartData.as_view(), name='chartdata')

]