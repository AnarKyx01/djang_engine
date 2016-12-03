from django.contrib import admin

# Register your models here.

from engine.models import Player, QuizLevel, Question, QuestionGet, Manager

admin.site.register(Player)
admin.site.register(Manager)
admin.site.register(QuizLevel)
admin.site.register(Question)
admin.site.register(QuestionGet)
