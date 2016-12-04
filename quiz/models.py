from django.db import models

import engine

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
	player = models.ForeignKey('engine.Player',
                                on_delete=models.CASCADE)
	solved_on = models.DateTimeField(auto_now_add = True, blank = True)

	def __str__(self):
		return "%s answered question on %s" % (self.player, self.solved_on)
