from django.conf.urls import url, include

from . import views

app_name = 'ctf'
urlpatterns = [
    #url(r'^level/unlock$', views.levelUnlock, name='levelUnlock'),
    url(r'^ctf/(?P<level>[0-9]+)/$', views.ctfLevel, name='level'),
    url(r'^ctf/(?P<level>[0-9]+)/submit$', views.flagSubmit, name='flagSubmit'),
]
