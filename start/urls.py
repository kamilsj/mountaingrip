from django.urls import path
from . import views
from apps.desire.views import DesireView

app_name = 'start'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:id>/', views.ProfileView.as_view(), name='user_profile'),
    path('profile/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('trip/', views.TripView.as_view(), name='trip'),
    path('trip/<int:id>/', views.TripView.as_view(), name='trip_quest'),
    path('trip/explore/', views.Explore.as_view(), name='explore'),
    path('add/', views.AddTrip.as_view(), name='add'),
    path('q/', views.q, name='q'),
    # some addition added to start view
    path('desire/', DesireView.as_view(), name='desire'),
]