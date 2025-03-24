from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.forms.array import SimpleArrayField
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from firmware_management.models import *
from firmware_management.choices import *
from extras.models import ConfigTemplate
from ipam.models import VRF, IPAddress
from netbox.choices import *
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import (
    CSVChoiceField, CSVContentTypeField, CSVModelChoiceField, CSVModelMultipleChoiceField, CSVTypedChoiceField,
    SlugField,
)
from virtualization.models import Cluster, VMInterface, VirtualMachine
from wireless.choices import WirelessRoleChoices
from jsonschema._keywords import required

class FirmwareImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        label=_('Manufacturer'),
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        help_text=_('Device type manufacturer')
    )
    device_type = CSVModelChoiceField(
        label=_('Device type'),
        queryset=DeviceType.objects.all(),
        required=False,
        to_field_name='model',
        help_text=_('Device type model')
    )
    status = CSVChoiceField(
        label=_('Status'),
        choices=DeviceStatusChoices,
        help_text=_('Operational status')
    )
    inventory_item_type = CSVModelChoiceField(
        label=_('Inventory item type'),
        queryset=InventoryItemType.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Inventory item type')
    )
    module_type = CSVModelChoiceField(
        label=_('Module type'),
        queryset=ModuleType.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Module type')
    )
    name = forms.CharField(
        label=_('Name'),
        help_text=_('Name of the firmware')
    )
    file_name = forms.CharField(
        label=_('File name'),
        required=False,
        help_text=_('File name of the firmware')
    )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        help_text=_('Description of the firmware')
    )
    comments = forms.CharField(
        label=_('Comments'),
        required=False,
        help_text=_('Additional comments about the firmware')
    )

    class Meta:
        model = Firmware
        fields = ['name', 'file_name', 'status', 'description', 'comments', 'manufacturer', 'device_type', 'inventory_item_type', 'module_type']
        labels = {
            'name': 'Name',
            'file_name': 'File name',
            'status': 'Status',
            'description': 'Description',
            'comments': 'Comments',
            'manufacturer': 'Manufacturer',
            'device_type': 'Device type',
            'inventory_item_type': 'Inventory item type',
            'module_type': 'Module type',
        }
        help_texts = {
            'name': 'Name of the firmware',
            'file_name': 'File name of the firmware',
            'status': 'Firmware lifecycle status',
            'description': 'Description of the firmware',
            'comments': 'Additional comments about the firmware',
            'manufacturer': 'The manufacturer which produces this device type',
            'device_type': 'The type of device',
            'inventory_item_type': 'The type of inventory item',
            'module_type': 'The type of module',
        }

    def clean(self):
        super().clean()
        # Perform additional validation on the form
        pass

class FirmwareAssignmentImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        label=_('Manufacturer'),
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        help_text=_('Device type manufacturer')
    )
    device_type = CSVModelChoiceField(
        label=_('Device type'),
        queryset=DeviceType.objects.all(),
        required=False,
        to_field_name='model',
        help_text=_('Device type model')
    )
    firmware = CSVModelChoiceField(
        label=_('Firmware'),
        queryset=Firmware.objects.all(),
        to_field_name='name',
        help_text=_('Firmware name')
    )
    module_type = CSVModelChoiceField(
        label=_('Module type'),
        queryset=ModuleType.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Module type')
    )
    inventory_item_type = CSVModelChoiceField(
        label=_('Inventory item type'),
        queryset=InventoryItemType.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Inventory item type')
    )
    device = CSVModelChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        to_field_name='name',
        help_text=_('Device name')
    )
    module = CSVModelChoiceField(
        label=_('Module'),
        queryset=Module.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Module name')
    )
    inventory_item = CSVModelChoiceField(
        label=_('Inventory item'),
        queryset=InventoryItem.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Inventory item name')
    )
    comments = forms.CharField(
        label=_('Comments'),
        required=False,
        help_text=_('Additional comments about the firmware assignment')
    )
    patch_date = forms.DateField(
        label=_('Patch date'),
        required=False,
        help_text=_('Date of the firmware patch')
    )
    ticket_number = forms.CharField(
        label=_('Ticket number'),
        required=False,
        help_text=_('Ticket number of the firmware patch')
    )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        help_text=_('Description of the firmware assignment')
    )

    class Meta:
        model = FirmwareAssignment
        fields = ['manufacturer', 'device_type', 'firmware', 'module_type', 'inventory_item_type', 'device', 'module', 'inventory_item', 'comments', 'patch_date', 'ticket_number', 'description']
        labels = {
            'firmware': 'Firmware',
            'manufacturer': 'Manufacturer',
            'device_type': 'Device type',
            'module_type': 'Module type',
            'inventory_item_type': 'Inventory item type',
            'device': 'Device',
            'module': 'Module',
            'inventory_item': 'Inventory item',
            'comments': 'Comments',
            'patch_date': 'Patch date',
            'ticket_number': 'Ticket number',
            'description': 'Description',
        }
        help_texts = {
            'firmware': 'Firmware name',
            'manufacturer': 'Device type manufacturer',
            'device_type': 'Device type model',
            'module_type': 'Module type',
            'inventory_item_type': 'Inventory item type',
            'device': 'Device name',
            'module': 'Module name',
            'inventory_item': 'Inventory item name',
            'comments': 'Additional comments about the firmware assignment',
            'patch_date': 'Date of the firmware patch',
            'ticket_number': 'Ticket number of the firmware patch',
            'description': 'Description of the firmware assignment',
        }

    def clean(self):
        super().clean()
        # Perform additional validation on the form
        pass