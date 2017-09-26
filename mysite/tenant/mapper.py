# -*- coding: utf-8 -*-
"""Maps a request to a tenant using the first part of the hostname.
For example:
  foo.example.com:8000 -> foo
  bar.baz.example.com -> bar
This is a simple example; you should probably verify tenant names
are valid before returning them, since the returned tenant name will
be issued in a `USE` SQL query.
"""

from db_multitenant import mapper
from db_multitenant import utils
from .models import DomainGroup


class TenantMapper(mapper.TenantMapper):

    def get_tenant_name(self, request, threadlocal):
        """Takes the first part of the hostname as the tenant"""
        #hostname = request.get_host().split(':')[0].lower()
        #return hostname.split('.')[0]

        # New implementation for retrieve tenant from database (on default schema: tenant_devnull)
        if "/admin/login" in request.path and request.method == "POST":
            username = request.POST["username"]
            try:
                domain = DomainGroup.objects.get(username=username)
                # Need to write picked tenantName in cookie
                threadlocal.set_write_cookie(True)
                return domain.tenantName

            except DomainGroup.DoesNotExist:
                return utils.get_default_tenant_name() # tenant par défaut

        # Maybe add extra security for avoid malicious cookie manipulation
        return request.COOKIES.get("tenant", utils.get_default_tenant_name())

    def get_dbname(self, request, threadlocal):
        # Refactor to avoid extra DomainGroup query
        return 'tenant_%s' % self.get_tenant_name(request, threadlocal)

    def get_cache_prefix(self, request, threadlocal):
        # Refactor to avoid extra DomainGroup query
        return 'tenant_%s' % self.get_tenant_name(request, threadlocal)