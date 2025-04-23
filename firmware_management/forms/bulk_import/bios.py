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

class BiosImportForm(NetBoxModelImportForm):
    hardware_kind = CSVTypedChoiceField(
        label=_('Hardware kind'),
        choices=HardwareKindChoices,
        required=True,
        help_text=_('Type of hardware')
    )
    hardware_name = forms.CharField(
        label=_('Hardware name'),
        required=True,
        help_text=_('Name of the hardware')
    )
    status = CSVChoiceField(
        label=_('Status'),
        choices=DeviceStatusChoices,
        help_text=_('Operational status')
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
        model = Bios
        fields = ['name', 'file_name', 'status', 'description', 'comments', 'device_type', 'module_type']
        labels = {
            'name': 'Name',
            'file_name': 'File name',
            'status': 'Status',
            'description': 'Description',
            'comments': 'Comments'
        }
        help_texts = {
            'name': 'Name of the firmware',
            'file_name': 'File name of the firmware',
            'status': 'Firmware lifecycle status',
            'description': 'Description of the firmware',
            'comments': 'Additional comments about the firmware'
        }

    def clean(self):
        super().clean()
        # Perform additional validation on the form
        pass
    
    def clean_hardware_name(self):
        hardware_kind = self.cleaned_data.get('hardware_kind')
        model = self.cleaned_data.get('hardware_name')
        if not hardware_kind:
            # clean on manufacturer or hardware_kind already raises
            return None
        if hardware_kind == 'device':
            hardware_class = DeviceType
            test = DeviceType.objects.get(model=model)
            print(test)
        elif hardware_kind == 'module':
            hardware_class = ModuleType
            test = ModuleType.objects.get(model=model)
            print(test)
        try:
            hardware_type = hardware_class.objects.get(model=model)
        except ObjectDoesNotExist:
            print(f'Hardware type not found: "{hardware_kind}", "{hardware_class}", "{model}"')
            raise forms.ValidationError(f'Hardware type not found: "{hardware_kind}", "{hardware_class}", "{model}"')
        setattr(self.instance, f'{hardware_kind}_type', hardware_type)
        return hardware_type

class BiosAssignmentImportForm(NetBoxModelImportForm):
    bios = CSVModelChoiceField(
        label=_('Bios'),
        queryset=Bios.objects.all(),
        to_field_name='name',
        help_text=_('Bios name')
    )
    device = CSVModelChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        required=False,
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
    comments = forms.CharField(
        label=_('Comments'),
        required=False,
        help_text=_('Additional comments about the bios assignment')
    )
    patch_date = forms.DateField(
        label=_('Patch date'),
        required=False,
        help_text=_('Date of the bios patch')
    )
    ticket_number = forms.CharField(
        label=_('Ticket number'),
        required=False,
        help_text=_('Ticket number of the bios patch')
    )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        help_text=_('Description of the bios assignment')
    )

    class Meta:
        model = BiosAssignment
        fields = ['bios', 'device', 'module', 'comments', 'patch_date', 'ticket_number', 'description']
        labels = {
            'bios': 'Bios',
            'device': 'Device',
            'module': 'Module',
            'comments': 'Comments',
            'patch_date': 'Patch date',
            'ticket_number': 'Ticket number',
            'description': 'Description',
        }
        help_texts = {
            'bios': 'Bios name',
            'device': 'Device name',
            'module': 'Module name',
            'comments': 'Additional comments about the bios assignment',
            'patch_date': 'Date of the bios patch',
            'ticket_number': 'Ticket number of the bios patch',
            'description': 'Description of the bios assignment',
        }

    def clean(self):
        super().clean()
        # Perform additional validation on the form
        pass