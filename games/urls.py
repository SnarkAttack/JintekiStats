from django.conf.urls import url

import views
from views import GameLogger, StatsViewer

app_name = 'games'
urlpatterns = [
    url(r'^$', views.list_games, name='list_games'),
    url(r'^record/$', views.record_game, name='record_game'),
    url(r'^log/$', GameLogger.as_view(), name='log_game'),
    url(r'^(?P<game_id>[0-9]+)/$', views.view_game, name='view_game'),
    url(r'^update-ids/$', views.get_ids, name='update_ids'),
    url(r'^stats/$', StatsViewer.as_view(), name='view_stats')
]
