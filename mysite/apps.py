# -*- coding: utf-8 -*-
from django.contrib.auth.apps import AuthConfig
from django.utils.translation import ugettext_lazy as _

class GypsyAuthConfig(AuthConfig):
    """ Renommage de l'application Auth (pour avoir un nom plus court)
    """
    verbose_name = _("Acces")
