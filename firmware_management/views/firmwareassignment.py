import logging
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.template import Template
from netbox.views import generic
from utilities.views import register_model_view

from .. import filtersets
from .. import tables
from .. import forms
from .. import models

__all__ = (
    'FirmwareAssignmentView',
    'FirmwareAssignmentListView',
    'FirmwareAssignmentChangeLogView',
    'FirmwareAssignmentJournalView'
)

@register_model_view(models.FirmwareAssignment)
class FirmwareAssignmentView(generic.ObjectView):
    queryset = models.FirmwareAssignment.objects.all()

    def get_extra_context(self, request, instance):
        context = super().get_extra_context(request, instance)
        return context

@register_model_view(models.FirmwareAssignment, 'list', path='', detail=False)
class FirmwareAssignmentListView(generic.ObjectListView):
    queryset = models.FirmwareAssignment.objects.prefetch_related(
        'manufacturer',
        'device_type',
        'inventory_item_type'
    )
    filterset = filtersets.FirmwareAssignmentFilterSet
    filterset_form = forms.FirmwareAssignmentFilterForm
    table = tables.FirmwareAssignmentTable
    
@register_model_view(models.FirmwareAssignment, 'edit')
@register_model_view(models.FirmwareAssignment, 'add', detail=False)
class FirmwareAssignmentEditView(generic.ObjectEditView):
    queryset = models.FirmwareAssignment.objects.all()
    form = forms.FirmwareAssignmentForm

class FirmwareAssignmentChangeLogView(generic.ObjectChangeLogView):
    """View for displaying the changelog of a FirmwareAssignment object"""
    queryset = models.FirmwareAssignment.objects.all()
    model = models.FirmwareAssignment

    def get(self, request, pk):
        return super().get(request, pk=pk, model=self.model)

class FirmwareAssignmentJournalView(generic.ObjectJournalView):
    """View for displaying the journal of a FirmwareAssignment object"""
    queryset = models.FirmwareAssignment.objects.all()
    model = models.FirmwareAssignment

    def get(self, request, pk):
        return super().get(request, pk=pk, model=self.model)

@register_model_view(models.FirmwareAssignment,'delete')
class FirmwareAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = models.FirmwareAssignment.objects.all()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@register_model_view(models.FirmwareAssignment, 'bulk_import', detail=False)
class FirmwareBulkImportView(generic.BulkImportView):
    queryset = models.FirmwareAssignment.objects.all()
    model_form = forms.FirmwareAssignmentImportForm

    def save_object(self, object_form, request):
        obj = object_form.save()
        return obj