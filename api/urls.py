from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('graph/', views.ChartData.as_view(), name='chartdata'),
    path('autocomplete/<str:query>/', views.Autocomplete.as_view(), name='autocomplete'),
    path('suggestions/', views.Suggestions.as_view(), name='suggestions'),
    path('notifications/<int:id>/',  views.Notifications.as_view(), name='notifications'),


    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]