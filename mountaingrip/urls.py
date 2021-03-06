from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from . import views
from .ajax import func

urlpatterns = [
    path('api/', include('api.urls')),
    path('ajax/checkmessages/<int:id>/', func.CheckMessages, name='check_messages'),
    path('ajax/addfriend/<int:id>/', func.AddFriend, name=''),
    path('ajax/jointrip/<int:id>/', func.JoinTrip, name=''),
    path('ajax/addpost/<int:id>/', func.AddPost, name=''),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate')
]

urlpatterns += i18n_patterns(
    path('', views.index, name='index'),
    path('start/', include('start.urls')),
    path('groups/', include('groups.urls')),
    path('inbox/', include('inbox.urls')),
    path('notifications/', include('notifications.urls')),
    path('admin/', admin.site.urls),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
)