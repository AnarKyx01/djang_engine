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


from .models import Player, FlagFind, Flag, CtfLevel, QuestionGet, Question, QuizLevel, Manager
# Create your views here.

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

class indexView(generic.ListView):
	template_name='engine/index.html'
	context_object_name = 'latest_finds_list'

	def get_queryset(self):
		return FlagFind.objects.filter(found_on__lte=timezone.now()).order_by('-found_on')[:5]

class scoreboardView(generic.ListView):
	template_name='engine/scoreboard.html'
	context_object_name = 'player_list'

	def get_queryset(self):
		return Player.objects.all().order_by('-score')

@user_passes_test(is_player)
def ctfLevel(request, level):
	levelObj = CtfLevel.objects.get(number = level)
	if level in request.user.player.ctfLevels:
		flags = Flag.objects.filter(level = levelObj)
		progress = levelObj.getProgressPercent(request.user.player)
		return render(request, 'engine/ctf_level.html', { 'flags':flags, 'level':levelObj, 'progress':progress })
	else:
		messages.warning(request, 'nooope')
		return HttpResponseRedirect(reverse('engine:index'))

@user_passes_test(is_player)
def quizLevel(request, level):
	levelObj = QuizLevel.objects.get(number = level)
	if level in request.user.player.quizLevels:
		questions = levelObj.getUnanswered(request.user.player)
		progress = levelObj.getProgressPercent(request.user.player)
		solved = request.user.player.getQuestions(levelObj)
		return render(request, 'engine/quiz_level.html', { 'questions':questions, 'solved':solved, 'level':levelObj, 'progress':progress })
	else:
		messages.warning(request, 'nooope')
		return HttpResponseRedirect(reverse('engine:index'))

@user_passes_test(is_player)
def levels(request):
	CtfLevels = request.user.player.getCtfLevels()
	QuizLevels = request.user.player.getQuizLevels()
	CtfLevels_count = len(request.user.player.getCtfLevels())
	QuizLevels_count = len(request.user.player.getQuizLevels())
	if CtfLevels_count >= 1 or QuizLevels_count >= 1:
		if CtfLevels_count >= 1:
			CtfLevels_query = CtfLevel.objects.filter(number__in=CtfLevels)
		else:
			CtfLevels_query = None
		if QuizLevels_count >= 1:
			Quizlevels_query = QuizLevel.objects.filter(number__in=QuizLevels)
		else:
			Quizlevels_query = None
		return render(request, 'engine/levels.html', { 'quiz_levels':Quizlevels_query, 'ctf_levels':CtfLevels_query})
	else:
		messages.warning(request, 'You currently do not have access to any levels')
		return render(request, 'engine/scoreboard.html')

@user_passes_test(is_player)
def flagSubmit(request, level):
	levelObj = CtfLevel.objects.get(number = level)
	flags = Flag.objects.filter(level = levelObj)
	progress = levelObj.getProgressPercent(request.user.player)
	if request.POST['notes'] == '':
		messages.warning(request, 'no notes = no points')
		return render(request, 'engine/ctf_level.html', { 'flags':flags, 'level':levelObj, 'progress':progress })
	try:
		flag_submit = flags.get(md5 = request.POST['flag_submission'])
	except(KeyError, Flag.DoesNotExist):
		messages.warning(request, 'Ahh.. nope')
		return render(request, 'engine/ctf_level.html', { 'flags':flags, 'level':levelObj, 'progress':progress })
	else:
		try:
			FlagFind.objects.filter(flag = flag_submit).get(player = request.user.player)
		except(KeyError, FlagFind.DoesNotExist):
			FlagFind(flag = flag_submit, notes = request.POST['notes'], player = request.user.player).save()
			u = request.user.player
			u.score += flag_submit.value
			u.save()
			messages.success(request, 'you rock, l33t h4x br0')
			return HttpResponseRedirect(reverse('engine:ctfLevel', args=(level)))
		else:
			messages.warning(request, 'Again? really....')
			return render(request, 'engine/ctf_level.html', { 'flags':flags, 'level':levelObj, 'progress':progress })

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
		return render(request, 'engine/quiz_level.html', { 'questions':questions, 'solved':solved, 'level':levelObj, 'progress':progress })
	else:
		if question_submit.answer != request.POST['answer_submission']:
			messages.warning(request, 'so close....')
			return render(request, 'engine/quiz_level.html', { 'questions':questions, 'solved':solved, 'level':levelObj, 'progress':progress })
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
				return HttpResponseRedirect(reverse('engine:quizLevel', args=(level)))
			else:
				messages.warning(request, 'Again? really....')
				return render(request, 'engine/quiz_level.html', { 'questions':questions, 'solved':solved, 'level':levelObj, 'progress':progress })

@user_passes_test(is_player)
def levelUnlock(request):
	if request.method == "POST":
		if request.POST['key'] == '':
			messages.warning(request, 'no key, bro... really?')
			return render(request, 'engine/unlock.html')
		try:
			unlocked = Level.objects.get(unlock_key = request.POST['key'])
		except(KeyError, Level.DoesNotExist):
			messages.warning(request, 'Ah ah ah.. you didn\' say the magic word')
			return render(request, 'engine/unlock.html')
		else:
			player = request.user.player
			if str(unlocked.number) in player.levels.split(','):
				messages.warning(request, 'you already unlocked that level...')
				return render(request, 'engine/unlock.html')
			else:
				player.levels += ',' + str(unlocked.number)
				player.save()
				messages.success(request, 'you rock, l33t h4x br0')
				return render(request, 'engine/unlock.html')
	else:
		return render(request, 'engine/unlock.html')

@user_passes_test(is_manager)
def managerConsole(request):
	players = Player.objects.all()
	player_count = players.count()
	levels = CtfLevel.objects.all()
	level_count = CtfLevel.objects.all().count()
	level_players = []
	level_progress = []
	player_tmp = Player.objects.all()

	for i in range(0, level_count, 1):
		player_tmp = player_tmp.filter(ctfLevels__contains=str(i))
		level_players.append(player_tmp.count())
		level_progress.append((float(player_tmp.count())/player_count)*100)

	level_progress = zip(levels, level_players, level_progress)

	return render(request, 'engine/manager_console.html', {'level_progress': level_progress, 'level_players':level_players, 'player_count':player_count, 'levels': levels})

@user_passes_test(is_manager)
def playerStats(request):

	return render(request, 'engine/playerStats.html')

@user_passes_test(is_manager)
def ctfLevelStats(request, level):
	player_count = Player.objects.all().count()
	level = CtfLevel.objects.get(number = level)
	level_players = Player.objects.filter(ctfLevels__icontains = level.number)
	level_player_count = Player.objects.filter(ctfLevels__icontains = level.number).count()
	if player_count != 0:
		level_player_percent = (float(level_player_count)/player_count)*100
	else:
		level_player_percent = 0
	players_completed = 0
	for player in level_players:
		player_flag_count = player.getFlags(level).count()
		level_flag_count = level.getFlagCount()
		if player_flag_count == level_flag_count:
			players_completed += 1

	if level_player_count != 0:
		player_completed_percent = (float(players_completed)/level_player_count)*100
	else:
		player_completed_percent = 0

	#level_flags = level.getFlags()
	level_flags = Flag.objects.filter(level = level)
	level_flag_finds = FlagFind.objects.filter(flag__in = level_flags)
	if level_flag_finds:
		first_find = FlagFind.objects.filter(flag__in = level_flags).order_by('found_on')[0]
		most_recent_find = FlagFind.objects.filter(flag__in = level_flags).order_by('-found_on')[0]
	else:
		first_find = "none"
		most_recent_find = "none"
	
	now = datetime.datetime.now()
	month_finds = []
	month_finds_count = []
	day_finds = []
	day_finds_count = []
	month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

	'''NOTE	!: must install pytz if using sqlite.. need to test with postgres'''

	for x in range(4,-1,-1):
		month_finds.append(month_names[now.month-x-1])
		month_finds_count.append(FlagFind.objects.filter(flag__in = level_flags).filter(found_on__month = now.month-x).count())
		day_finds.append(str(now.day-x)+' '+month_names[now.month-1])
		day_finds_count.append(FlagFind.objects.filter(flag__in = level_flags).filter(found_on__day = now.day-x).count())

	print (month_finds)
	print (month_finds_count)
	print (day_finds)
	print (day_finds_count)

	level_stats = {
					"level":level,
					"player_count":player_count,
					"level_player_count":level_player_count,
					#"level_player_percent":level_player_percent,
					"players_completed":players_completed,
					#"player_completed_percent":player_completed_percent,
					"first_find":first_find,
					"most_recent_find":most_recent_find,
					"month_finds":month_finds,
					"month_finds_count":month_finds_count,
					"day_finds":day_finds,
					"day_finds_count":day_finds_count

				}

	level_flag_find_count = []
	level_flag_find_percent = []
	for flag in level_flags:
		level_flag_find_count.append(FlagFind.objects.filter(flag = flag).count())
		if level_player_count != 0:
			level_flag_find_percent.append((level_flag_find_count[-1]/float(level_player_count))*100)
		else:
			player_completed_percent = level_flag_find_percent.append(0)
	flag_stats = zip(level_flags, level_flag_find_count, level_flag_find_percent)

	return render(request, 'engine/level_stats.html', { 'level_stats':level_stats, 'flag_stats':flag_stats })