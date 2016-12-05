from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator

''' User Models '''

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=25)
    score = models.IntegerField(default=0)
    ctfLevels = models.CharField(validators=[int_list_validator], max_length=50, null=True, blank=True)
    quizLevels = models.CharField(default="0", validators=[int_list_validator], max_length=50)

    def getCtfLevels(self):
        return list(filter(None, self.ctfLevels.split(',')))

    def getQuizLevels(self):
        return list(filter(None, self.quizLevels.split(',')))

    def getFlags(self):
        return FlagFind.objects.filter(player=self)

    def getFlags(self, level):
        flags = Flag.objects.filter(level=level)
        return FlagFind.objects.filter(player=self).filter(flag__in=flags)

    def unlockLevel(self, level):
        self.ctfLevels.append(',' + level)

    def getQuestions(self):
        return QuestionGet.objects.filter(player=self)

    def getQuestions(self, level):
        questions = Question.objects.filter(level=level)
        return QuestionGet.objects.filter(player=self).filter(question__in=questions)

    def last_seen(self):
        return self.user.last_login

    def __str__(self):
        return self.handle


class Manager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	handle = models.CharField(max_length=25)

	def __str__(self):
		return self.handle
