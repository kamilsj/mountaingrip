from django.urls import path, include
from rest_framework import routers
from apps.api.desire.desire_api import Desire
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('graph/', views.ChartData.as_view(), name='chartdata'),
    path('autocomplete/search/', views.Autocomplete.as_view(), name='autocomplete'),
    path('autocomplete/trip/<str:what>', views.Autocomplete.as_view(), name='autocomplete'),
    path('autocomplete/inbox/', views.AutocompleteInbox.as_view(), name='autocomplete_inbox'),
    path('suggestions/', views.Suggestions.as_view(), name='suggestions'),
    path('notifications/<int:id>/',  views.Notifications.as_view(), name='notifications'),
    path('desire/', Desire.as_view(), name='desire'),
    path('shop/', include('api.shop.urls'), name='shop'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]