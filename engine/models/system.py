from django.db import models

from .ctf import Flag

''' Systems '''

class Systems(models.Model):
    system = models.OneToOneField(Flag, on_delete=models.CASCADE)

    def getSystemCount(self):
        return Flag.objects.filter(target_ip=self).count()

    def getSystems(self):
        return Flag.objects.filter(target_ip=self)

    def __str__(self):
        return self.system, self.getSystemCount
