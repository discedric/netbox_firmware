from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from netbox_firmware.models import *
from netbox_firmware.choices import *
from netbox.choices import *
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import (
    CSVChoiceField, CSVContentTypeField, CSVModelChoiceField, CSVModelMultipleChoiceField, CSVTypedChoiceField,
    SlugField,
)

### Firmware ###


class FirmwareImportForm(NetBoxModelImportForm):
    name = forms.CharField(
        label=_('Name'),
        required=True,
        help_text=_('Name of the firmware')
    )
    manufacturer = CSVModelChoiceField(
        label=_('Manufacturer'),
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        required=True,
        help_text=_('Firmware type manufacturer')
    )
    file_name = forms.CharField(
        label=_('File name'),
        required=False,
        help_text=_('File name of the firmware')
    )
    hardware_kind = CSVChoiceField(
        label=_('Hardware kind'),
        choices=HardwareKindChoices,
        required=True,
        help_text=_('Type of hardware')
    )
    hardware_type_name = CSVModelMultipleChoiceField(
        label=_('Hardware Type name'),
        queryset=DeviceType.objects.all(),
        to_field_name='model',
        required=False,
        help_text=_('Name of the hardware Type')
    )
    device_type = CSVModelMultipleChoiceField(
        label=_('Device Type name'),
        queryset=DeviceType.objects.all(),
        to_field_name='model',
        required=False,
        help_text=_('Name of the Device Type')
    )
    module_type = CSVModelMultipleChoiceField(
        label=_('Module Type name'),
        queryset=ModuleType.objects.all(),
        to_field_name='model',
        required=False,
        help_text=_('Name of the Module Type')
    )
    status = CSVChoiceField(
        label=_('Status'),
        choices=FirmwareStatusChoices,
        required=False,
        help_text=_('Operational status')
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
        fields = [
            'name', 
            'file_name', 
            'status', 
            'description', 
            'comments', 
            'manufacturer', 
            'hardware_kind', 
            'hardware_type_name',
            'device_type',
            'module_type',
            ]
        

    def clean(self):
        super().clean()
        # Perform additional validation on the form
        pass

    def _clean_fields(self):
        return super()._clean_fields()

    # def _get_validation_exclusions(self):
    #     exclude = super()._get_validation_exclusions()
    #     exclude.remove('device_type')
    #     exclude.remove('module_type')
    #     return exclude

    # def clean_hardware_type_name(self):
    #     hardware_kind = self.cleaned_data.get('hardware_kind')
    #     manufacturer = self.cleaned_data.get('manufacturer')
    #     models = self.cleaned_data.get('hardware_type_name')  # list of names from CSV

    #     if not hardware_kind or not manufacturer:
    #         return None

    #     if hardware_kind == 'device':
    #         hardware_class = DeviceType
    #         field_name = 'device_type'
    #     elif hardware_kind == 'module':
    #         hardware_class = ModuleType
    #         field_name = 'module_type'
    #     else:
    #         raise forms.ValidationError(f'Unknown hardware kind: {hardware_kind}')

    #     hardware_types = []
    #     for model_name in models:
    #         try:
    #             obj = hardware_class.objects.get(
    #                 manufacturer=manufacturer,
    #                 model=model_name
    #             )
    #             hardware_types.append(obj)
    #         except hardware_class.DoesNotExist:
    #             raise forms.ValidationError(
    #                 f'Hardware type not found: kind={hardware_kind}, '
    #                 f'manufacturer={manufacturer}, model="{model_name}"'
    #             )

    #     # assign to the ManyToMany field (must save instance first in bulk import flow)
    #     self.instance.save()
    #     getattr(self.instance, field_name).set(hardware_types)

    #     return hardware_types


     ##########



    # def clean_hardware_type_name(self):
    #     hardware_kind = self.cleaned_data.get('hardware_kind')
    #     manufacturer = self.cleaned_data.get('manufacturer')
    #     model = self.cleaned_data.get('hardware_type_name')
    #     if not hardware_kind or not manufacturer:
    #         # clean on manufacturer or hardware_kind already raises
    #         return None
    #     if hardware_kind == 'device':
    #         hardware_class = DeviceType
    #     elif hardware_kind == 'module':
    #         hardware_class = ModuleType
    #     try:
    #         hardware_type = hardware_class.objects.get(
    #             manufacturer=manufacturer, model=model
    #         )
    #     except ObjectDoesNotExist:
    #         raise forms.ValidationError(
    #             f'Hardware type not found: "{hardware_kind}", "{manufacturer}", "{model}"'
    #         )
    #     setattr(self.instance, f'{hardware_kind}_type', hardware_type)
    #     return hardware_type

    def _get_clean_value(self, field_name):
        try:
            return self.base_fields[field_name].clean(self.data.get(field_name))
        except forms.ValidationError as e:
            self.add_error(field_name, e)
            raise


### FirmwareAssignment ###


class FirmwareAssignmentImportForm(NetBoxModelImportForm):
    firmware = CSVModelChoiceField(
        label=_('Firmware'),
        queryset=Firmware.objects.all(),
        to_field_name='name',
        help_text=_('Firmware name')
    )
    manufacturer = CSVModelChoiceField(
        label=_('Manufacturer'),
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        help_text=_('Device type manufacturer')
    )
    hardware_kind = CSVTypedChoiceField(
        label=_('Hardware kind'),
        choices=HardwareKindChoices,
        required=True,
        help_text=_('Type of hardware')
    )
    hardware_name = forms.CharField(
        label=_('Hardware name'),
        required=True,
        help_text=_('Name of the hardware, e.g. device name or module id/serial')
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
        fields = [
            'firmware', 
            'manufacturer', 
            'hardware_kind', 
            'hardware_name', 
            'comments', 
            'patch_date', 
            'ticket_number', 
            'description'
            ]

    def clean(self):
        super().clean()
        pass
    
    def _clean_fields(self):
        return super()._clean_fields()

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        exclude.remove('device')
        exclude.remove('module')
        return exclude

    def clean_hardware_name(self):
        hardware_kind = self.cleaned_data.get('hardware_kind')
        manufacturer = self.cleaned_data.get('manufacturer')
        model = self.cleaned_data.get('hardware_name')

        if not hardware_kind or not manufacturer:
            return None

        try:
            if hardware_kind == 'device':
                hardware_type = Device.objects.get(
                    device_type__manufacturer=manufacturer, name=model
                )
                existing = FirmwareAssignment.objects.filter(device__name=model).first()
                if existing and existing.id != self.instance.id:
                    raise ValidationError(f'Device "{model}" already has a Firmware assigned.')

            elif hardware_kind == 'module':
                if model.isdigit():
                    hardware_type = Module.objects.get(
                        module_type__manufacturer=manufacturer, pk=model
                    )
                    existing = FirmwareAssignment.objects.filter(module__pk=model).first()
                else:
                    hardware_type = Module.objects.get(
                        module_type__manufacturer=manufacturer, serial=model
                    )
                    existing = FirmwareAssignment.objects.filter(module__serial=model).first()

                if existing and existing.id != self.instance.id:
                    raise ValidationError(f'Module "{model}" already has a Firmware assigned.')

        except ObjectDoesNotExist:
            raise forms.ValidationError(
                f'Hardware type not found: "{hardware_kind}", "{manufacturer}", "{model}"'
            )

        setattr(self.instance, f'{hardware_kind}', hardware_type)
        return hardware_type

    def _get_clean_value(self, field_name):
        try:
            return self.base_fields[field_name].clean(self.data.get(field_name))
        except forms.ValidationError as e:
            self.add_error(field_name, e)
            raise