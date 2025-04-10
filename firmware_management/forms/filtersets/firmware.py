from django import forms
from django.utils.translation import gettext_lazy as _

from dcim.choices import DeviceStatusChoices
from dcim.models import DeviceType, Manufacturer, ModuleType, InventoryItem, Device, Module
from netbox.choices import *
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, FilterForm, add_blank_choice
from utilities.forms.fields import ColorField, DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import NumberWithOptions
from wireless.choices import *
from firmware_management.models import Firmware, FirmwareAssignment

class FirmwareFilterForm(NetBoxModelFilterSetForm):
    model = Firmware
    fieldsets = (
        FieldSet('q', 'tag', name=_('General')),
        FieldSet('status',name=_('Status')),
        FieldSet('manufacturer_id', 'device_type_id', 'module_type_id', name=_('Hardware')),
    )
    
    selector_fields = ('q', 'status', 'manufacturer_id')
    
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer')
    )
    device_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
        label=_('Device Type')
    )
    module_type_id = DynamicModelMultipleChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
        label=_('Module Type')
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=DeviceStatusChoices,
        required=False
    )
    tag = TagFilterField(model)
    

class FirmwareAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = FirmwareAssignment
    fieldsets = (
        FieldSet('q', 'tag'),
        FieldSet('patch_date',name=_('Patch Date')),
        FieldSet('manufacturer_id', 'device_type_id', 'module_type_id', 'device_id', 'module_id', 'inventory_item_id',name=_('Hardware')), 
        FieldSet('firmware_id',name=_('Firmware')),
    )
    
    selector_fields = ('q', 'patch_date', 'manufacturer_id', 'device_type_id', 'module_type_id', 'device_id', 'module_id', 'inventory_item_id', 'firmware_id')
    
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer')
    )
    device_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
        label=_('Device Type')
    )
    module_type_id = DynamicModelMultipleChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
        label=_('Module Type')
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'device_type_id': '$device_type_id'
        },
        label=_('Device')
    )
    module_id = DynamicModelMultipleChoiceField(
        queryset=Module.objects.all(),
        required=False,
        query_params={
            'module_type_id': '$module_type_id'
        },
        label=_('Module')
    )
    inventory_item_id = DynamicModelMultipleChoiceField(
        queryset=InventoryItem.objects.all(),
        required=False,
        label=_('Inventory Item')
    )
    firmware_id = DynamicModelMultipleChoiceField(
        queryset=Firmware.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id',
            'device_type_id': '$device_type_id'
        },
        label=_('Firmware')
    )
    patch_date = forms.DateField(
        label=_('Patch Date'),
        required=False
    )
    tag = TagFilterField(model)