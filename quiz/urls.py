
from django.conf.urls import url, include

from django.contrib.auth import views as auth_views

from . import views

app_name = 'quiz'
urlpatterns = [
	url(r'^quiz/(?P<level>[0-9]+)/$', views.quizLevel, name='level'),
	url(r'^quiz/(?P<level>[0-9]+)/submit$', views.questionSubmit, name='questionSubmit'),
]
