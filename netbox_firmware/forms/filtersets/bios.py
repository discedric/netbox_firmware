from django import forms
from django.utils.translation import gettext_lazy as _

from netbox_firmware.choices import BiosStatusChoices,HardwareKindChoices
from dcim.models import DeviceType, Manufacturer, ModuleType, Device, Module
from netbox.choices import *
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, FilterForm, add_blank_choice
from utilities.forms.fields import ColorField, DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import NumberWithOptions, DatePicker
from wireless.choices import *
from netbox_firmware.models import Bios, BiosAssignment

class BiosFilterForm(NetBoxModelFilterSetForm):
    model = Bios
    fieldsets = (
        FieldSet('q', 'tag', name=_('General')),
        FieldSet('manufacturer_id', 'status', name=_('BIOS')),
        FieldSet('kind', 'device_type_id', 'module_type_id', name=_('Hardware')),
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
        label=_('Device Type'),
    )
    module_type_id = DynamicModelMultipleChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
        label=_('Module Type'),
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=BiosStatusChoices,
        required=False
    )
    kind = forms.MultipleChoiceField(
        label=_('Kind'),
        choices=HardwareKindChoices,
        required=False
    )
    tag = TagFilterField(model)
    

class BiosAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = BiosAssignment
    fieldsets = (
        FieldSet('q', 'tag'),
        FieldSet('patch_date',name=_('Patch Date')),
        FieldSet('manufacturer_id', 'kind', 'device_type_id', 'device_id', 'module_type_id', 'module_id', 'module_sn','module_device_id', name=_('Hardware')), 
        FieldSet('bios_id',name=_('BIOS')),
    )
    
    selector_fields = ('q', 'patch_date', 'manufacturer_id', 'device_id', 'module_id', 'bios_id')
    
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer')
    )
    kind = forms.MultipleChoiceField(
        label=_('Kind'),
        choices=HardwareKindChoices,
        required=False
    )
    device_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        label=_('Device Type'),
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id',
            'device_type_id': '$device_type_id',
            'module_type_id': '$module_type_id'
        },
        label=_('Device')
    )
    module_type_id = DynamicModelMultipleChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        label=_('Module Type'),
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
    )
    module_id = DynamicModelMultipleChoiceField(
        queryset=Module.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id',
            'device_type_id': '$device_type_id',
            'module_type_id': '$module_type_id'
        },
        label=_('Module')
    )
    module_sn = forms.CharField(
        required=False,
        label=_('Module Serial Number')
    )
    module_device_id = forms.ModelMultipleChoiceField(
        queryset=Device.objects.filter(modules__isnull=False).distinct(),
        required=False,
        label=_('Module Owner')
    )
    bios_id = DynamicModelMultipleChoiceField(
        queryset=Bios.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id',
            'device_id': '$device_id',
            'module_id': '$module_id'
        },
        label=_('BIOS'),
    )
    patch_date = forms.DateField(
        label=_('Patch Date'),
        required=False,
        widget=DatePicker()
    )
    tag = TagFilterField(model)