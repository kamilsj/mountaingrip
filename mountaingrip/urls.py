from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from . import views
from .ajax import func

'''Error views'''
from django.conf.urls import handler404, handler500, handler403, handler400

handler400 = 'mountaingrip.views.error_404'
handler403 = 'mountaingrip.views.error_403'
handler404 = 'mountaingrip.views.error_404'
handler500 = 'mountaingrip.views.error_500'


urlpatterns = [
    path('api/', include('apps.api.urls')),
    path('ajax/checknotifications/', func.CheckNotifications, name='check_messages'),
    path('ajax/addfriend/<int:id>/', func.AddFriend, name=''),
    path('ajax/jointrip/<int:id>/', func.JoinTrip, name=''),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate')
]

urlpatterns += i18n_patterns(
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('start/', include('start.urls')),
    path('groups/', include('apps.groups.urls')),
    path('inbox/', include('apps.inbox.urls')),
    path('health/', include('apps.health.urls')),
    path('shop/', include('apps.shop.urls')),                        #store
    path('ranking/', include('apps.ranking.urls')),                  #user's ranking
    path('notifications/', include('apps.notifications.urls')),
    path('ejp/', include('apps.ejp.urls')),                          #ejp analysis ... just to make some new content and learn something new
    path('admin/', admin.site.urls),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
)