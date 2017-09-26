# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Document

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    pass
    list_display = ['__unicode__', 'fichier']
    search_fields = ['name']

    def has_add_permission(self, request):
        '''
        Pour ne permettre qu'un seul enregistrement
        '''
        # if there's already an entry, do not allow adding
        return not Document.objects.exists()

admin.site.register(Document, DocumentAdmin)
