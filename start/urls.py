from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('profile/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('trip/', views.TripView.as_view(), name='trip'),
    path('trip/<int:id>/', views.TripView.as_view(), name='trip_quest'),
    path('trip/explore/', views.explore, name='explore'),
    path('add/', views.AddTrip.as_view(), name='add'),
    path('q/', views.q, name='q'),
]