from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url
from . import views
from .ajax import func

urlpatterns = [
    path('api/', include('api.urls')),
    path('ajax/addfriend/<int:id>/', func.AddFriend, name=''),
    path('ajax/jointrip/<int:id>/', func.JoinTrip, name=''),
    path('ajax/addpost/<int:id>/', func.AddPost, name=''),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate')
]

urlpatterns += i18n_patterns(
    path('', views.index, name='index'),
    path('start/', include('start.urls')),
    path('admin/', admin.site.urls),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
)