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
    'FirmwareAssignmentView',
    'FirmwareAssignmentListView',
    'FirmwareAssignmentBulkCreateView'
)

@register_model_view(models.Firmware)
class FirmwareAssignmentView(generic.ObjectView):
    queryset = models.Firmware.objects.all()

    def get_extra_context(self, request, instance):
        context = super().get_extra_context(request, instance)
        return context

@register_model_view(models.Firmware, 'list', path='', detail=False)
class FirmwareAssignmentListView(generic.ObjectListView):
    queryset = models.Firmware.objects.prefetch_related(
        'manufacturer',
        'device_type',
        'inventory_item_type'
    )
    table = tables.FirmwareTable
    
@register_model_view(models.Firmware, 'bulk_add', path='bulk-add', detail=False)
class FirmwareAssignmentBulkCreateView(generic.BulkCreateView):
    queryset = models.Firmware.objects.all()
    form = forms.FirmwareBulkAddForm
    model_form = forms.FirmwareBulkAddModelForm
    pattern_target = None
    template_name = 'firmware_management/firmware_assignment_bulk_add.html'

    def _create_objects(self, form, request):
        new_objects = []
        for _ in range(form.cleaned_data['count']):
            # Reinstantiate the model form each time to avoid overwriting the same instance. Use a mutable
            # copy of the POST QueryDict so that we can update the target field value.
            model_form = self.model_form(request.POST.copy())
            del(model_form.data['count'])

            # Validate each new object independently.
            if model_form.is_valid():
                obj = model_form.save()
                new_objects.append(obj)
            else:
                # Raise an IntegrityError to break the for loop and abort the transaction.
                raise IntegrityError()

        return new_objects
    
@register_model_view(models.Firmware, 'edit')
@register_model_view(models.Firmware, 'add', detail=False)
class FirmwareAssignmentEditView(generic.ObjectEditView):
    queryset = models.Firmware.objects.all()
    form = forms.FirmwareForm
    template_name = 'firmware_management/firmware_assignment_edit.html'