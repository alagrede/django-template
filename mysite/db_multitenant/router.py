from db_multitenant import utils

class DatabaseRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'DomainGroup':
            return utils.get_default_tenant_name()
        else:
            if utils.get_threadlocal().get_tenant_name() == None:
                return utils.get_default_tenant_name()
            else:
                return utils.get_threadlocal().get_tenant_name()

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'DomainGroup':
            return utils.get_default_tenant_name()
        else:
            if utils.get_threadlocal().get_tenant_name() == None:
                return utils.get_default_tenant_name()
            else:
                return utils.get_threadlocal().get_tenant_name()

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_syncdb(self, db, model):
        return True