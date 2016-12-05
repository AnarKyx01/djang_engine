from django.contrib import admin

# Register your models here.

from engine.models import users, ctf, quiz, system

admin.site.register(users.Player)
admin.site.register(users.Manager)
admin.site.register(ctf.CtfLevel)
admin.site.register(ctf.Flag)
admin.site.register(ctf.FlagFind)
admin.site.register(quiz.QuizLevel)
admin.site.register(quiz.Question)
admin.site.register(quiz.QuestionGet)
