from django.urls import path
from . import views

app_name = 'public'
urlpatterns = [
    path('', views.PublicIndex.as_view(), name='public_index'),
    path('trip/<int:id>/', views.PublicTrip.as_view(), name='public_trip'),
    path('profile/<int:id>/', views.PublicProfile.as_view(), name='public_profile'),
]