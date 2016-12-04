from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import QuizLevel, Question, QuestionGet

def is_player(user):
	try:
		return user.player is not None
	except ObjectDoesNotExist:
		return False

def is_manager(user):
	try:
		return user.manager is not None
	except ObjectDoesNotExist:
		return False

@user_passes_test(is_player)
def quizLevel(request, level):
	levelObj = QuizLevel.objects.get(number = level)
	if level in request.user.player.quizLevels:
		questions = levelObj.getUnanswered(request.user.player)
		progress = levelObj.getProgressPercent(request.user.player)
		solved = request.user.player.getQuestions(levelObj)
		return render(request, 'quiz/quiz_level.html', { 'questions':questions, 'solved':solved, 'level':levelObj, 'progress':progress })
	else:
		messages.warning(request, 'nooope')
		return HttpResponseRedirect(reverse('engine:index'))

@user_passes_test(is_player)
def questionSubmit(request, level):
	levelObj = QuizLevel.objects.get(number = level)
	questions = levelObj.getUnanswered(request.user.player)
	progress = levelObj.getProgressPercent(request.user.player)
	solved = request.user.player.getQuestions(levelObj)
	progress = levelObj.getProgressPercent(request.user.player)

	try:
		question_submit = Question.objects.get(id = request.POST['question_id'])
	except(KeyError, Question.DoesNotExist):
		messages.warning(request, 'Ahh.. that question doesn\'t exist...')
		return render(request, 'quiz/quiz_level.html', { 'questions':questions, 'solved':solved, 'level':levelObj, 'progress':progress })
	else:
		if question_submit.answer != request.POST['answer_submission']:
			messages.warning(request, 'so close....')
			return render(request, 'quiz/quiz_level.html', { 'questions':questions, 'solved':solved, 'level':levelObj, 'progress':progress })
		else:
			try:
				QuestionGet.objects.filter(question = question_submit).get(player = request.user.player)
			except(KeyError, QuestionGet.DoesNotExist):
				QuestionGet(question = question_submit, player = request.user.player).save()
				u = request.user.player
				u.score += question_submit.value
				if levelObj.getProgressPercent(request.user.player) >= 75:
					if '0' not in request.user.player.getCtfLevels():
						u.ctfLevels = '0'
				u.save()
				messages.success(request, 'you rock, l33t h4x br0')
				return HttpResponseRedirect(reverse('quiz:level', args=(level)))
			else:
				messages.warning(request, 'Again? really....')
				return render(request, 'quiz/quiz_level.html', { 'questions':questions, 'solved':solved, 'level':levelObj, 'progress':progress })
