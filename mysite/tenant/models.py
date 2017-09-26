# -*- coding: utf-8 -*-
from django.db import models


class DomainGroup(models.Model):

    username = models.CharField(max_length=50, unique=True)
    tenantName = models.CharField(max_length=50)

    def __unicode__(self):              # __unicode__ on Python 2
        return u"%s - %s" % (self.username, self.tenantName)

