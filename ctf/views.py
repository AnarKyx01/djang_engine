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

from .models import CtfLevel, Flag, FlagFind, FlagAttempt

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
def ctfLevel(request, level):
	levelObj = CtfLevel.objects.get(number = level)
	if level in request.user.player.ctfLevels:
		flags = Flag.objects.filter(level = levelObj)
		progress = levelObj.getProgressPercent(request.user.player)
		return render(request, 'ctf/ctf_level.html', { 'flags':flags, 'level':levelObj, 'progress':progress })
	else:
		messages.warning(request, 'nooope')
		return HttpResponseRedirect(reverse('engine:index'))

@user_passes_test(is_player)
def flagSubmit(request, level):
	levelObj = CtfLevel.objects.get(number = level)
	flags = Flag.objects.filter(level = levelObj)
	progress = levelObj.getProgressPercent(request.user.player)
	if request.POST['notes'] == '':
		messages.warning(request, 'no notes = no points')
		return render(request, 'ctf/ctf_level.html', { 'flags':flags, 'level':levelObj, 'progress':progress })
	try:
		flag_submit = flags.get(md5 = request.POST['flag_submission'])
	except(KeyError, Flag.DoesNotExist):
		messages.warning(request, 'Ahh.. nope')
		return render(request, 'ctf/ctf_level.html', { 'flags':flags, 'level':levelObj, 'progress':progress })
	else:
		try:
			FlagFind.objects.filter(flag = flag_submit).get(player = request.user.player)
		except(KeyError, FlagFind.DoesNotExist):
			FlagFind(flag = flag_submit, notes = request.POST['notes'], player = request.user.player).save()
			u = request.user.player
			u.score += flag_submit.value
			u.save()
			messages.success(request, 'you rock, l33t h4x br0')
			return HttpResponseRedirect(reverse('ctf:level', args=(level)))
		else:
			messages.warning(request, 'Again? really....')
			return render(request, 'ctf/ctf_level.html', { 'flags':flags, 'level':levelObj, 'progress':progress })
