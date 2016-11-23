from django.contrib import admin

# Register your models here.

from engine.models import Player, CtfLevel, Flag, QuizLevel, Question, FlagFind, QuestionGet, Manager

admin.site.register(Player)
admin.site.register(Manager)
admin.site.register(CtfLevel)
admin.site.register(Flag)
admin.site.register(FlagFind)
admin.site.register(QuizLevel)
admin.site.register(Question)
admin.site.register(QuestionGet)
