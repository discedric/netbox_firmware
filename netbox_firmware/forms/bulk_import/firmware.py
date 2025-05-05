from django import forms
from django.utils.translation import gettext_lazy as _

from netbox_firmware.models import *
from netbox_firmware.choices import *
from netbox.choices import *
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import (
    CSVChoiceField, CSVContentTypeField, CSVModelChoiceField, CSVModelMultipleChoiceField, CSVTypedChoiceField,
    SlugField,
)
from jsonschema._keywords import required

class FirmwareImportForm(NetBoxModelImportForm):
    """_summary_
    Zorgen dat we de hardware type en model meegeven in plaats van de 3 dingen appart
    
    """
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
        choices=FirmwareStatusChoices,
        help_text=_('Operational status')
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
        fields = ['name', 'file_name', 'status', 'description', 'comments', 'manufacturer', 'device_type', 'module_type']
        labels = {
            'name': 'Name',
            'file_name': 'File name',
            'status': 'Status',
            'description': 'Description',
            'comments': 'Comments',
            'manufacturer': 'Manufacturer',
            'device_type': 'Device type',
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
            'module_type': 'The type of module',
        }

    def clean(self):
        clean_data = super().clean()
        # Perform additional validation on the form
        return clean_data

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
        to_field_name='id',
        help_text=_('Module id')
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
        fields = ['manufacturer', 'device_type', 'firmware', 'module_type', 'device', 'module', 'comments', 'patch_date', 'ticket_number', 'description']
        labels = {
            'firmware': 'Firmware',
            'manufacturer': 'Manufacturer',
            'device_type': 'Device type',
            'module_type': 'Module type',
            'device': 'Device',
            'module': 'Module',
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
            'device': 'Device name',
            'module': 'Module id',
            'comments': 'Additional comments about the firmware assignment',
            'patch_date': 'Date of the firmware patch',
            'ticket_number': 'Ticket number of the firmware patch',
            'description': 'Description of the firmware assignment',
        }

    def clean(self):
        clean_data = super().clean()
        module = self.cleaned_data.get('module')
        device = self.cleaned_data.get('device')
        # Perform additional validation on the form
        if FirmwareAssignment.objects.filter(module=module).exists():
            raise ValidationError(f'Module "{module}" already has a BIOS assigned.')
        if FirmwareAssignment.objects.filter(device=device).exists():
            raise ValidationError(f'Device "{device}" already has a BIOS assigned.')
        return clean_data