# coding: utf-8

from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld

from ckeditor.widgets import CKEditorWidget


class FlatpageForm(FlatpageFormOld):

    def __init__(self, *args, **kwargs):
        super(FlatpageForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = CKEditorWidget()
        self.fields['sites'].label = 'Сайты'

    class Meta:
        model = FlatPage
        exclude = []


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

