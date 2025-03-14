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