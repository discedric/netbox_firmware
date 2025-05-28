from django import forms
from django.utils.translation import gettext_lazy as _

from netbox_firmware.choices import FirmwareStatusChoices,HardwareKindChoices
from dcim.models import DeviceType, Manufacturer, ModuleType, Device, Module
from netbox.choices import *
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, FilterForm, add_blank_choice
from utilities.forms.fields import ColorField, DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import NumberWithOptions
from wireless.choices import *
from netbox_firmware.models import Firmware, FirmwareAssignment

class FirmwareFilterForm(NetBoxModelFilterSetForm):
    model = Firmware
    fieldsets = (
        FieldSet('q', 'tag', name=_('General')),
        FieldSet('status',name=_('Status')),
        FieldSet('kind', 'manufacturer_id', 'device_type_id', 'module_type_id', name=_('Hardware')),
    )
    
    selector_fields = ('q', 'status', 'manufacturer_id', 'device_type_id', 'module_type_id')
    
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
        choices=FirmwareStatusChoices,
        required=False
    )
    kind = forms.MultipleChoiceField(
        choices=HardwareKindChoices,
        required=False,
        label=_('Kind')
    )
    tag = TagFilterField(model)
    

class FirmwareAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = FirmwareAssignment
    fieldsets = (
        FieldSet('q', 'tag'),
        FieldSet('patch_date',name=_('Patch Date')),
        FieldSet('kind', 'manufacturer_id', 'device_type_id', 'module_type_id', 'device_id', 'module_id','module_device_id', name=_('Hardware')), 
        FieldSet('firmware_id',name=_('Firmware')),
    )
    
    selector_fields = ('q', 'patch_date', 'manufacturer_id', 'device_id', 'module_id', 'firmware_id')
    
    kind = forms.MultipleChoiceField(
        label=_('Kind'),
        choices=HardwareKindChoices,
        required=False
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer')
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'device_type__manufacturer_id': '$manufacturer_id'
        },
        label=_('Device')
    )
    module_id = DynamicModelMultipleChoiceField(
        queryset=Module.objects.all(),
        required=False,
        query_params={
            'module_type__manufacturer_id': '$manufacturer_id'
        },
        label=_('Module')
    )
    module_device_id = forms.ModelMultipleChoiceField(
        queryset=Device.objects.filter(modules__isnull=False).distinct(),
        required=False,
        label=_('Module Owner')
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
    firmware_id = DynamicModelMultipleChoiceField(
        queryset=Firmware.objects.all(),
        required=False,
        query_params={
            'device_id': '$device_id',
            'module_id': '$module_id'
        },
        label=_('Firmware')
    )
    patch_date = forms.DateField(
        label=_('Patch Date'),
        required=False
    )
    tag = TagFilterField(model)