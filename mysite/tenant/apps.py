from django.apps import AppConfig


class TenantConfig(AppConfig):
    name = 'tenant'
    verbose_name = 'Tenant'

    def ready(self):
        import tenant.signals