from django import forms
from django.utils.translation import gettext_lazy as _

from dcim.choices import DeviceStatusChoices
from dcim.models import DeviceType, Manufacturer, ModuleType, InventoryItem, Device, Module
from netbox_inventory.models import InventoryItemType
from netbox.choices import *
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, FilterForm, add_blank_choice
from utilities.forms.fields import ColorField, DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import NumberWithOptions
from wireless.choices import *
from firmware_management.models import Bios, BiosAssignment

class BiosFilterForm(NetBoxModelFilterSetForm):
    model = Bios
    fieldsets = (
        FieldSet('q', 'tag', name=_('General')),
        FieldSet('status',name=_('Status')),
        FieldSet('device_type_id', 'module_type_id', 'inventory_item_type_id', name=_('Hardware')),
    )
    
    selector_fields = ('q', 'status')
    
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer')
    )
    device_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        label=_('Device Type'),
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
    )
    module_type_id = DynamicModelMultipleChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        label=_('Module Type'),
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
    )
    inventory_item_type_id = DynamicModelMultipleChoiceField(
        queryset=InventoryItemType.objects.all(),
        required=False,
        label=_('Inventory Item Type'),
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=DeviceStatusChoices,
        required=False
    )
    tag = TagFilterField(model)
    

class BiosAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = BiosAssignment
    fieldsets = (
        FieldSet('q', 'tag'),
        FieldSet('patch_date',name=_('Patch Date')),
        FieldSet('device_id', 'module_id', 'inventory_item_id',name=_('Hardware')), 
        FieldSet('bios_id',name=_('Bios')),
    )
    
    selector_fields = ('q', 'patch_date', 'device_id', 'module_id', 'inventory_item_id', 'bios_id')
    
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer')
    )

    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_('Device'),
        query_params={
            'device_type__manufacturer_id': '$manufacturer_id'
        },
    )
    module_id = DynamicModelMultipleChoiceField(
        queryset=Module.objects.all(),
        required=False,
        label=_('Module'),
        query_params={
            'module_type__manufacturer_id': '$manufacturer_id'
        },
    )
    inventory_item_id = DynamicModelMultipleChoiceField(
        queryset=InventoryItem.objects.all(),
        required=False,
        label=_('Inventory Item'),
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
    )
    bios_id = DynamicModelMultipleChoiceField(
        queryset=Bios.objects.all(),
        required=False,
        label=_('Bios'),
        query_params={
            'device__device_type__manufacturer_id': '$manufacturer_id',
            'module__module_type__manufacturer_id': '$manufacturer_id',
            'inventory_item__manufacturer_id': '$manufacturer_id',
            'device_id': '$device_id',
            'module_id': '$module_id',
            'inventory_item_id': '$inventory_item_id'
        },
    )
    patch_date = forms.DateField(
        label=_('Patch Date'),
        required=False
    )
    tag = TagFilterField(model)