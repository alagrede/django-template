# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from django.forms import TextInput, Textarea
from django.db import models
from datetime import datetime
import os

# Register your models here.
from mysite import settings
from django.contrib.auth.models import User
from .models import Task
from fusion import print_process
from fusion.models import Document

#https://github.com/yourlabs/django-autocomplete-light
from autocomplete_light import shortcuts

#https://django-salmonella.readthedocs.org/en/latest/
from salmonella.admin import SalmonellaMixin


#======================================================
# Task Actions Custom 
#   - Génération des fusions
#   - téléchargement en masse 
#   - suppression des fusions avec tâches
#======================================================

def delete_task(modeladmin, request, queryset):
    """ Supprime les taches et fusions sélectionnées
    """
    for task in queryset:
        task_name = "RESULT_" + str(task.id).replace("/","-") + "_fusion.docx"
        if os.path.exists(settings.FILE_OUT_DOC + task_name):
            os.remove(settings.FILE_OUT_DOC + task_name)
        task.delete()
delete_task.short_description = "Delete tasks and documents"


def download_docs(modeladmin, request, queryset):
    """ Téléchargement des fusions
    """
    from fusion import views
    import zipfile
    import datetime

    filename = settings.FILE_SYSTEM_TMP + str(datetime.datetime.today().strftime('%d%m%Y-%H%M%S')) + ".zip"
    # Création de l'archive
    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as z:

        # Ajout des factures sélectionnées à l'archive
        for task in queryset:
            task_name = "RESULT_" + str(task.id).replace("/","-") + "_fusion.docx"
            print 
            if os.path.exists(settings.FILE_OUT_DOC + task_name):
                z.write(settings.FILE_OUT_DOC + task_name, arcname = "TSK_" + task_name)

    # Téléchargement du zip des documents
    return views.__getdoc__(filename)
download_docs.short_description = "Download documents"


def make_fusion(modeladmin, request, queryset):
    for task in queryset:
        modelename = Document.objects.get(id=1).fichier.name # On utilise le premier modèle pour l'exemple
        print_process.make_print(task, modelename)
        
        task.printed_doc = True # On signale que la tache est imprimée
        task.save()
make_fusion.short_description = "Print documents"


#======================================================
# Task Filters
#======================================================
# Pour générer la liste des dates
def gen_range(start, stop, step):
    current = start
    while current < stop:
        next_current = current + step
        if next_current < stop:
            yield (current, current)
        else:
            yield (current, stop)
        current = next_current


class DateRangeFilter(admin.SimpleListFilter):
    """ Filtre custom pour filtrer les Taches sur une période
    """
    title = _('Date')
    parameter_name = 'date'

    def lookups(self, request, model_admin):        
        return gen_range(2015,2050,1)

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(date__year=self.value())


class StateFilter(admin.SimpleListFilter):
    """ Filtre custom pour afficher les taches en fonction de leur état
    """
    title = _('Etat')
    parameter_name = 'state'

    def lookups(self, request, model_admin):
        return (
                (1, _("Todo")),
                (2, _("Done")),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(state=self.value())




#======================================================
# Task Admin
#======================================================

class TaskAdmin(SalmonellaMixin, admin.ModelAdmin):

    
    ####################################################################
    # Pour transformer la sélection de l'author par une sélection avec popup de recherche
    ####################################################################
    #raw_id_fields = ('author',)
    #salmonella_fields = ('author',)


    #Filtre les relations 
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(is_active=True) # Montrer uniquement les utilisateurs actifs
        return super(TaskAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #Pour initialiser des valeurs par défaut dans le formulaire
    def get_form(self, request, obj=None, *args, **kwargs):
        form = super(TaskAdmin, self).get_form(request, *args, **kwargs)
        # Initial values
        #form.base_fields['obj'].initial = "Hello"        
        return form


    # Affichage tabulaire (1 onglet)
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('date', 'obj', 'state', 'author')
        }),
    )
    suit_form_tabs = (('general', _('Info')), )


    list_display = ['__unicode__', 'date', 'obj', 'author', 'printed_doc'] #, 'action_link'
    search_fields = ['obj']
    list_filter = [DateRangeFilter, StateFilter]
    actions = [delete_task, download_docs, make_fusion]

    # Pour effacer l'action de suppression par défaut
    def get_actions(self, request):
        actions = super(TaskAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


    ####################################################################
    # Génére un lien de suppression pour chaque ligne dans la liste
    ####################################################################
    #def action_link(self, obj):
    #    """ Pour rajouter un lien de suppression de l'item dans la liste
    #    """
    #    app_name = obj._meta.app_label
    #    url_name = obj._meta.model_name
    #    data_id = obj.id
    #
    #    return """
    #            <a href="/admin/{0}/{1}/{2}/delete"><i class="icon-remove"></i><span class="sronly">Delete</span></a>
    #         """.format(
    #         obj._meta.app_label, 
    #         obj._meta.model_name, 
    #         obj.id)
    #action_link.allow_tags = True
    #action_link.short_description = _('Actions')


    ####################################################################
    # Pour transformer la sélection de l'author en autocomplete
    ####################################################################
    #https://github.com/yourlabs/django-autocomplete-light
    #form = shortcuts.modelform_factory(Task, exclude=[])


admin.site.register(Task, TaskAdmin)


