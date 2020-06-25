from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('trip/', views.trip, name='trip'),
    path('trip/<int:id>/', views.trip, name='trip'),
    path('trip/explore/', views.explore, name='explore'),
    path('add/', views.AddTrip.as_view(), name='add'),
    path('q/', views.q, name='q')
]