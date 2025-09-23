from django import forms
from django.utils.translation import gettext_lazy as _

from dcim.models import DeviceType, Manufacturer, ModuleType, Device, Module
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from utilities.forms.widgets import DatePicker
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms import add_blank_choice

from netbox_firmware.choices import FirmwareStatusChoices
from netbox_firmware.models import (
    Firmware,
    FirmwareAssignment
)

class FirmwareBulkEditForm(NetBoxModelBulkEditForm):
    name = forms.CharField(required=False, label='Name')
    status = forms.ChoiceField(
        choices=add_blank_choice(FirmwareStatusChoices),
        required=False,
        label='Status',
    )
    description = forms.CharField(
        required=False,
    )
    file_name = forms.CharField(required=False, label='File Name')
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        selector=True,
        label='Manufacturer'
    )
    device_type = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
        label='Supported Device Type',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    add_device_type = DynamicModelMultipleChoiceField(
        label=_('Add Device Type'),
        queryset=DeviceType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    remove_device_type = DynamicModelMultipleChoiceField(
        label=_('Remove Device Type'),
        queryset=DeviceType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer',
        }
    )
    module_type = DynamicModelMultipleChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        selector=True,
        label='Supported Module Type',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    add_module_type = DynamicModelMultipleChoiceField(
        label=_('Add Module Type'),
        queryset=ModuleType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    remove_module_type = DynamicModelMultipleChoiceField(
        label=_('Remove Module Type'),
        queryset=ModuleType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer',
        }
    )
    comments = CommentField()
    


    model = Firmware
    fieldsets=(
        FieldSet('name', 'manufacturer', 'file_name', 'status', 'description',name='General'),
        FieldSet(
            TabbedGroups(
                FieldSet('device_type', name=_('Fixed Assignment')),
                FieldSet('add_device_type', 'remove_device_type', name=_('Add/Remove')),
            ),
            name='Device Type'
        ),
        FieldSet(
            TabbedGroups(
                FieldSet('module_type', name=_('Fixed Assignment')),
                FieldSet('add_module_type', 'remove_module_type', name=_('Add/Remove')),
            ),
            name='Module Type'
        ),
    )
    nullable_fields = ['device_type', 'module_type']
    

class FirmwareAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        required=False,
    )
    
    # Hardware Items ------------------------
    
    device = DynamicModelChoiceField(
        queryset = Device.objects.all(),
        required=False,
        selector=True,
        label='Device',
    )
    module = DynamicModelChoiceField(
        queryset = Module.objects.all(),
        required=False,
        selector=True,
        label='Module',
    )
    
    # Update --------------------------------
    firmware = DynamicModelChoiceField(
        queryset=Firmware.objects.all(),
        selector=True,
        required=False,
        label='Firmware',
    )
    comment = CommentField()
    patch_date = forms.DateField(
        widget=DatePicker(attrs={'is_clearable': True}),
        required=False,
        label='Patch Date',
        help_text='Date of the firmware patch'
    )
    ticket_number = forms.CharField(
        required=False,
        label='Ticket Number',
        help_text='Ticket number for the firmware patch'
    )
    
    model= FirmwareAssignment
    fieldsets = (
        FieldSet(
            'manufacturer','description',
            TabbedGroups(
                FieldSet('device',name='Device'),
                FieldSet('module',name='Module'),
            ),
            name='Hardware'
        ),
        FieldSet(
            'ticket_number','firmware','patch_date','comment',
            name='Update'
        ),
    )
    nullable_fields = ['device', 'module', 'ticket_number', 'patch_date', 'comment']