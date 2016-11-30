
from django.conf.urls import url, include

from django.contrib.auth import views as auth_views

from . import views

app_name = 'engine'
urlpatterns = [
	url(r'^$', views.indexView.as_view(), name='index'),
	url(r'^scoreboard/$', views.scoreboardView.as_view(), name='scoreboard'),
	#url(r'^scoreboard/(?P<pk>[0-9]+)/$', views.userScoreView, name='userScore'),
	url(r'^level/$', views.levels, name='levels'),
	url(r'^level/unlock$', views.levelUnlock, name='levelUnlock'),
	url(r'^ctf/(?P<level>[0-9]+)/$', views.ctfLevel, name='ctfLevel'),
	url(r'^ctf/(?P<level>[0-9]+)/submit$', views.flagSubmit, name='flagSubmit'),
	url(r'^quiz/(?P<level>[0-9]+)/$', views.quizLevel, name='quizLevel'),
	url(r'^quiz/(?P<level>[0-9]+)/submit$', views.questionSubmit, name='questionSubmit'),
	url(r'^login/$', auth_views.login, {'template_name': 'engine/login.html'}, name='login'),
	url(r'^logout/$', auth_views.logout, name='logout'),
	url(r'^manage/$', views.managerConsole, name='managerConsole'),
	#url(r'^stats/level/$', views.levelStatsList, name='levelStatsList'),
	url(r'^stats/ctf/(?P<level>[0-9]+)/$', views.ctfLevelStats, name='levelStats'),
	url(r'^stats/ctf/chart/(?P<level>[0-9])/$', views.ctfStatsChart, name="ctfStatsChart"),
]
