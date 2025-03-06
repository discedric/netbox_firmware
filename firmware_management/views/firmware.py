import logging
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.template import Template
from netbox.views import generic
from utilities.views import register_model_view

from .. import tables
from .. import forms
from .. import models
from ..template_content import WARRANTY_PROGRESSBAR

__all__ = (
    'FirmwareView',
    'FirmwareListView'
)

@register_model_view(models.Firmware)
class FirmwareView(generic.ObjectView):
    queryset = models.Firmware.objects.all()

    def get_extra_context(self, request, instance):
        context = super().get_extra_context(request, instance)
        context['warranty_progressbar'] = Template(WARRANTY_PROGRESSBAR)
        return context

@register_model_view(models.Firmware, 'list', path='', detail=False)
class FirmwareListView(generic.ObjectListView):
    queryset = models.Firmware.objects.prefetch_related(
        'manufacturer',
        'device_type',
        'inventory_item_type'
    )
    table = tables.FirmwareTable
    
@register_model_view(models.Firmware, 'edit')
@register_model_view(models.Firmware, 'add', detail=False)
class FirmwareEditView(generic.ObjectEditView):
    queryset = models.Firmware.objects.all()
    form = forms.FirmwareForm
    template_name = 'firmware_management/firmware_edit.html'