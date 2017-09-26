# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext 
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

# Create your models here.

states = (
    (1,_('Todo')),
    (2,_('Done')),
)


class Task(models.Model):
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    #Information générales
    date = models.DateField(null=True,verbose_name=_("Date"))
    obj = models.CharField(max_length=200, null=True, verbose_name = _("Object"))
    state = models.SmallIntegerField(choices = states, null=True, blank=False,verbose_name=_("State"))
    author = models.ForeignKey(User, related_name='auteur', verbose_name = _("Author"))

    printed_doc = models.BooleanField(default=False, verbose_name="printed document")

    def as_json(self):
        result = dict()
        result['id'] = self.id
        result['date'] = str(self.date.strftime("%d-%m-%Y"))
        result['obj'] = self.obj
        result['author'] = self.author.username
        return result

    #ajout pour salmonella
    def classname(self):
        return self.__class__.__name__.lower()

    def __unicode__(self):              # __unicode__ on Python 2
        return (self.obj[:30] + '..') if len(self.obj) > 30 else self.obj

