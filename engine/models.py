from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import int_list_validator
# Create your models here.

''' User Models '''

class Player(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	handle = models.CharField(max_length=25)
	score = models.IntegerField(default=0)
	ctfLevels = models.CharField(validators=[int_list_validator], max_length=50, null = True, blank = True)
	quizLevels = models.CharField(default="0", validators=[int_list_validator], max_length=50)

	def getCtfLevels(self):
		return list(filter(None, self.ctfLevels.split(',')))

	def getQuizLevels(self):
		return list(filter(None, self.quizLevels.split(',')))

	def getFlags(self):
		return FlagFind.objects.filter(player = self)

	def getFlags(self, level):
		flags = Flag.objects.filter(level = level)
		return FlagFind.objects.filter(player = self).filter(flag__in = flags)

	def unlockLevel(self, level):
		self.ctfLevels.append(','+level)

	def getQuestions(self):
		return QuestionGet.objects.filter(player = self)

	def getQuestions(self, level):
		questions = Question.objects.filter(level = level)
		return QuestionGet.objects.filter(player = self).filter(question__in = questions)

	def __str__(self):
		return self.handle


class Manager(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	handle = models.CharField(max_length=25)

	def __str__(self):
		return self.handle


''' Quiz Level Models '''

class QuizLevel(models.Model):

	number = models.IntegerField(default=0, unique=True)
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField(default='')
	unlock_key = models.CharField(max_length=32, unique=True)

	def getQuestionCount(self):
		return Question.objects.filter(level=self).count()

	def getQuestions(self):
		Question.objects.filter(level=self)

	def getProgressPercent(self, player):
		count = self.getQuestionCount()
		if count == 0:
			return 0
		player_count = player.getQuestions(self).count()
		return (float(player_count)/count)*100

	def getUnanswered(self, player):
		players_questions = player.getQuestions(self)
		return Question.objects.filter(level=self).exclude(questionget__in = players_questions)

	def getAnswered(self, player):
		players_questions = player.getQuestions(self)
		return QuestionGet.objects.filter(level=self).filter(questionget__in = players_questions)

	def __str__(self):
		return self.name

class Question(models.Model):

	answer = models.CharField(max_length = 50, unique=True)
	description = models.TextField(default='')
	level = models.ForeignKey(QuizLevel, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length = 25, unique=True)
	question_text = models.TextField(default='')
	value = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class QuestionGet(models.Model):
	question = models.ForeignKey(Question)
	player = models.ForeignKey(Player)
	solved_on = models.DateTimeField(auto_now_add = True, blank = True)

	def __str__(self):
		return "%s answered question on %s" % (self.player, self.solved_on)

''' CTF Level Models '''

class CtfLevel(models.Model):

	number = models.IntegerField(default=0, unique=True)
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField(default='')
	unlock_key = models.CharField(max_length=32, unique=True)

	def getFlagCount(self):
		return Flag.objects.filter(level=self).count()

	def getFlags(self):
		Flag.objects.filter(level=self)

	def getProgressPercent(self, player):
		count = self.getFlagCount()
		if count == 0:
			return 0
		player_count = player.getFlags(self).count()
		return (float(player_count)/count)*100

	def __str__(self):
		return self.name

class Flag(models.Model):

	description = models.TextField(default='')
	level = models.ForeignKey(CtfLevel, on_delete=models.CASCADE, null=True)
	md5 = models.CharField(max_length = 32, unique=True)
	name = models.CharField(max_length = 25, unique=True)
	target_ip = models.GenericIPAddressField(protocol = 'IPv4')
	value = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class FlagFind(models.Model):
	flag = models.ForeignKey(Flag)
	player = models.ForeignKey(Player)
	found_on = models.DateTimeField(auto_now_add = True, blank = True)
	notes = models.TextField(default='')

	def __str__(self):
		return "%s found a flag on %s" % (self.player, self.found_on)
