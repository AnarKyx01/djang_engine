
from django.conf.urls import url, include

from django.contrib.auth import views as auth_views

from .views import engine, ctf, quiz

app_name = 'engine'
urlpatterns = [
	url(r'^$', engine.indexView.as_view(), name='index'),
	url(r'^scoreboard/$', engine.scoreboardView.as_view(), name='scoreboard'),
	#url(r'^scoreboard/(?P<pk>[0-9]+)/$', views.userScoreView, name='userScore'),
	url(r'^level/$', engine.levels, name='levels'),
	url(r'^login/$', auth_views.login, {'template_name': 'engine/login.html'}, name='login'),
	url(r'^logout/$', auth_views.logout, name='logout'),
	url(r'^manage/$', engine.managerConsole, name='managerConsole'),
	#url(r'^stats/level/$', views.levelStatsList, name='levelStatsList'),
	url(r'^stats/ctf/(?P<level>[0-9]+)/$', engine.ctfLevelStats, name='levelStats'),
	url(r'^stats/ctf/chart/(?P<level>[0-9])/$', engine.ctfStatsChart, name="ctfStatsChart"),
	url(r'^systems/$', engine.systemsView, name='Systems'),
	url(r'^quiz/(?P<level>[0-9]+)/$', quiz.quizLevel, name='level'),
	url(r'^quiz/(?P<level>[0-9]+)/submit$', quiz.questionSubmit, name='questionSubmit'),
    url(r'^ctf/(?P<level>[0-9]+)/$', ctf.ctfLevel, name='level'),
	url(r'^ctf/(?P<level>[0-9]+)/submit$', ctf.flagSubmit, name='flagSubmit'),
]
