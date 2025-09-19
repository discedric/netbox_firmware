import logging
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.template import Template
from netbox.views import generic
from utilities.query import count_related
from utilities.views import register_model_view, ViewTab

from ..utils import get_countdevice
from .. import tables
from .. import forms
from .. import models
from .. import filtersets

__all__ = (
    'FirmwareView',
    'FirmwareListView',
)

@register_model_view(models.Firmware)
class FirmwareView(generic.ObjectView):
    queryset = models.Firmware.objects.all()

    def get_extra_context(self, request, instance):
        context = super().get_extra_context(request, instance)
        return context

@register_model_view(models.Firmware, 'list', path='', detail=False)
class FirmwareListView(generic.ObjectListView):
    queryset = models.Firmware.objects.prefetch_related(
        'device_type',
        'module_type'
    ).annotate(
        instance_count=count_related(models.FirmwareAssignment,'firmware'),
    )
    filterset = filtersets.FirmwareFilterSet
    filterset_form = forms.FirmwareFilterForm
    table = tables.FirmwareTable

@register_model_view(models.Firmware, 'edit')
@register_model_view(models.Firmware, 'add', detail=False)
class FirmwareEditView(generic.ObjectEditView):
    queryset = models.Firmware.objects.all()
    form = forms.FirmwareForm
    default_return_url = 'plugins:netbox_firmware:firmware_list'

@register_model_view(models.Firmware,'delete')
class FirmwareDeleteView(generic.ObjectDeleteView):
    queryset = models.Firmware.objects.all()
    default_return_url = 'plugins:netbox_firmware:firmware_list'
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# ----------------- Bulk Import, Edit, Delete -----------------

@register_model_view(models.Firmware, 'bulk_import', detail=False)
class FirmwareBulkImportView(generic.BulkImportView):
    queryset = models.Firmware.objects.all()
    model_form = forms.FirmwareImportForm

    def save_object(self, object_form, request):
        obj = object_form.save()
        return obj
    
@register_model_view(models.Firmware, 'bulk_edit', detail=False)
class FirmwareBulkEditView(generic.BulkEditView):
    queryset = models.Firmware.objects.all()
    filterset = filtersets.FirmwareFilterSet
    table = tables.FirmwareTable
    form = forms.FirmwareBulkEditForm
    default_return_url = 'plugins:netbox_firmware:firmware_list'
    
    def post_save_operations(self, form, obj):
        super().post_save_operations(form, obj)

        # Add/remove Linked Device Types
        if form.cleaned_data.get('add_device_type', None):
            obj.device_type.add(*form.cleaned_data['add_device_type'])
        if form.cleaned_data.get('remove_device_type', None):
            obj.device_type.remove(*form.cleaned_data['remove_device_type'])

        # Add/remove Linked Module Types
        if form.cleaned_data.get('add_module_type', None):
            obj.module_type.add(*form.cleaned_data['add_module_type'])
        if form.cleaned_data.get('remove_module_type', None):
            obj.module_type.remove(*form.cleaned_data['remove_module_type'])

    def post (self, request, **kwargs):
        return super().post(request, **kwargs)


@register_model_view(models.Firmware, 'bulk_delete', detail=False)
class FirmwareBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Firmware.objects.all()
    table = tables.FirmwareTable

    def post(self, request):
        return super().post(request)