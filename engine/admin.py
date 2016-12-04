from django.contrib import admin

# Register your models here.

from engine.models import Player, Manager

admin.site.register(Player)
admin.site.register(Manager)
