# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Document(models.Model):
    class Meta:
        verbose_name = _("Model")
        verbose_name_plural = _("Models")

    fichier = models.FileField(upload_to='upload/', verbose_name = _("File"))
    name = models.CharField(max_length=200, unique=True, verbose_name = _("Document name"))
    

    def __unicode__(self):              # __unicode__ on Python 2
        return u"{}".format(self.name)
