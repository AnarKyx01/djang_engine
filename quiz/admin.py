from django.contrib import admin

from quiz.models import QuizLevel, Question, QuestionGet

admin.site.register(QuizLevel)
admin.site.register(Question)
admin.site.register(QuestionGet)
