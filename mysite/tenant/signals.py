# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import connections
from db_multitenant import utils

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def check_user_not_exist_in_public(cursor, username):
    cursor.execute("SELECT username FROM "+ get_databasePrefix() +"tenant_domaingroup WHERE username = %s", [username])
    row = cursor.fetchone()
    return row is None


def get_databasePrefix():
    if utils.get_mode() == "SCHEMA":
        return "tenant_"+utils.get_default_tenant_name()+"."
    return ""

@receiver(pre_save, sender=get_user_model())
def model_pre_save(sender, **kwargs):

    """
    Contenu du la méthode:
    si user creation
        -> vérifier sur public que username not exist
            -> si oui INSERT
            -> si non raise existUsername
    si user update
        -> vérifier sur public que new_username not exist
            -> si oui UPDATE public avec le new_username
    """

    threadlocal = utils.get_threadlocal()
    client_tenant = threadlocal.get_tenant_name()

    cursor = connections["default"].cursor()

    if kwargs['instance'].id is not None: # update
        #if kwargs["update_fields"] is not None and "login" in kwargs["update_fields"]:
            old_username = get_user_model().objects.get(id=kwargs['instance'].id).username
            if kwargs['instance'].username != old_username:
                if check_user_not_exist_in_public(cursor, kwargs['instance'].username):
                    # No one with this username
                    # Transaction is handle by Djange save() method
                    cursor.execute("UPDATE " + get_databasePrefix() + "tenant_domaingroup SET username=%s WHERE username=%s", [kwargs['instance'].username, old_username])
                else:
                    raise AlreadyExistUsernameException("Username %s alerady exist" % kwargs['instance'].username)

    else: # création
        if check_user_not_exist_in_public(cursor, kwargs['instance'].username):
            # No one with this username
            # Transaction is handle by Djange save() method
            cursor.execute("INSERT INTO " + get_databasePrefix() + "tenant_domaingroup(username, tenantName) VALUES(%s, %s)", [kwargs['instance'].username, client_tenant])
        else:
            raise AlreadyExistUsernameException("Username %s alerady exist" % kwargs['instance'].username)


@receiver(post_delete, sender=get_user_model())
def model_post_delete(sender, **kwargs):
    logger.info('Deleted: {}'.format(kwargs['instance'].__dict__))

    username = kwargs['instance'].username

    cursor = connections["default"].cursor()
    cursor.execute("DELETE FROM " + get_databasePrefix() + "tenant_domaingroup  WHERE username=%s", [username])



class AlreadyExistUsernameException(Exception):
    pass