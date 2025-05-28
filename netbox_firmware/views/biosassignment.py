import logging
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.template import Template
from utilities.query import count_related
from netbox.views import generic
from utilities.views import register_model_view

from netbox_firmware import filtersets
from netbox_firmware import tables
from netbox_firmware import forms
from netbox_firmware import models

__all__ = (
    'BiosAssignmentView',
    'BiosAssignmentListView',
)

@register_model_view(models.BiosAssignment)
class BiosAssignmentView(generic.ObjectView):
    queryset = models.BiosAssignment.objects.all()

    def get_extra_context(self, request, instance):
        context = super().get_extra_context(request, instance)
        return context

@register_model_view(models.BiosAssignment, 'list', path='', detail=False)
class BiosAssignmentListView(generic.ObjectListView):
    queryset = models.BiosAssignment.objects.prefetch_related(
        'device',
        'module',
        'bios',
    )
    filterset = filtersets.BiosAssignmentFilterSet
    filterset_form = forms.BiosAssignmentFilterForm
    table = tables.BiosAssignmentTable
    
@register_model_view(models.BiosAssignment, 'edit')
@register_model_view(models.BiosAssignment, 'add', detail=False)
class BiosAssignmentEditView(generic.ObjectEditView):
    queryset = models.BiosAssignment.objects.all()
    form = forms.BiosAssignmentForm
    default_return_url = 'plugins:netbox_firmware:biosassignment_list'

@register_model_view(models.BiosAssignment,'delete')
class BiosAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = models.BiosAssignment.objects.all()
    default_return_url = 'plugins:netbox_firmware:biosassignment_list'
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# ----------------- Bulk Import, Edit, Delete -----------------

@register_model_view(models.BiosAssignment, 'bulk_import', detail=False)
class BiosBulkImportView(generic.BulkImportView):
    queryset = models.BiosAssignment.objects.all()
    model_form = forms.BiosAssignmentImportForm

    def save_object(self, object_form, request):
        obj = object_form.save()
        return obj

@register_model_view(models.BiosAssignment, 'bulk_edit', detail=False)
class BiosAssignmentBulkEditView(generic.BulkEditView):
    queryset = models.BiosAssignment.objects.all()
    filterset = filtersets.BiosAssignmentFilterSet
    table = tables.BiosAssignmentTable
    form = forms.BiosAssignmentBulkEditForm
    default_return_url = 'plugins:netbox_firmware:biosassignment_list'
    
    def post (self, request, **kwargs):
        return super().post(request, **kwargs)

@register_model_view(models.BiosAssignment, 'bulk_delete', detail=False)
class BiosAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = models.BiosAssignment.objects.all()
    table = tables.BiosAssignmentTable

    def post(self, request):
        return super().post(request)