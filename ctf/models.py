from django.db import models

import engine

# Create your models here.

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
	player = models.ForeignKey('engine.Player',
                                on_delete=models.CASCADE,)
	found_on = models.DateTimeField(auto_now_add = True, blank = True)
	notes = models.TextField(default='')

	def __str__(self):
		return "%s found a flag on %s" % (self.player, self.found_on)

class FlagAttempt(models.Model):
    flag_attempt = models.ForeignKey(Flag)
    player = models.ForeignKey('engine.Player',
                                on_delete=models.CASCADE,)
    attempt_on = models.DateTimeField(auto_now_add = True, blank = True)
    level = models.ForeignKey(CtfLevel)

    def __str__(self):
        return "%s attempted to submit %s for level %s on %s" % (self.player, self.flag_attempt, self.level, self.attempt_on)
