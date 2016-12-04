from django.contrib import admin

from .models import CtfLevel, Flag, FlagFind, FlagAttempt

# Register your models here.

admin.site.register(CtfLevel)
admin.site.register(Flag)
admin.site.register(FlagFind)
