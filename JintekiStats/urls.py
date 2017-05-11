from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^games/', include('games.urls', namespace='games')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', auth_views.login, name='login'),
    url(r'^acounts/logout/', auth_views.logout, {'next_page': '/login/'}, name='logout'),
]
