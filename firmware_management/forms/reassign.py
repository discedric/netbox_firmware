from django import forms 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from firmware_management.models import Firmware, FirmwareAssignment

from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import DatePicker 

from dcim.models import Device, Module, InventoryItem
from dcim.choices import DeviceStatusChoices

__all__ = (

)


class FirmwareReassignMixin(forms.Form):
    """
    A mixin form for reassigning firmware to devices, modules, and inventory items.
    """
    patch_date = forms.DateField(
        required=False,
        widget=DatePicker(),
        label='Patch Date',
        help_text='The date when the firmware was patched.',
    )
    ticket_number = forms.CharField(
        required=False,
        max_length=100,
        label='Ticket Number',
        help_text='The ticket number associated with this firmware reassignment.',
    )
    comment = CommentField(
        required=False,
        label='Comment',
        help_text='Additional comments about the reassignment.',
    )

    class Meta:
        model = FirmwareAssignment
        fields = ['firmware', 'patch_date', 'ticket_number', 'comment']

    def save(self, commit=True):
        """
        Save the firmware assignment. Create a new assignment if none exists,
        or update the existing assignment.
        """
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate."
                % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )

        # Determine the hardware type (device, module, or inventory item)
        hardware_type = self.hardware_type
        hardware_instance = getattr(self.instance, hardware_type, None)

        # Check if an existing FirmwareAssignment exists
        firmware_assignment = FirmwareAssignment.objects.filter(
            **{hardware_type: hardware_instance}
        ).first()

        if firmware_assignment:
            # Update the existing assignment
            firmware_assignment.firmware = self.cleaned_data['firmware']
            firmware_assignment.patch_date = self.cleaned_data.get('patch_date')
            firmware_assignment.ticket_number = self.cleaned_data.get('ticket_number')
            firmware_assignment.comment = self.cleaned_data.get('comment')
        else:
            # Create a new assignment
            firmware_assignment = FirmwareAssignment(
                firmware=self.cleaned_data['firmware'],
                patch_date=self.cleaned_data.get('patch_date'),
                ticket_number=self.cleaned_data.get('ticket_number'),
                comment=self.cleaned_data.get('comment'),
                **{hardware_type: hardware_instance},
            )

        if commit:
            firmware_assignment.save()

        return firmware_assignment

    def clean(self):
        """
        Validate the reassignment of firmware to the specified hardware type.
        """
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        print(cleaned_data)
        # Ensure the firmware is provided
        firmware = cleaned_data['firmware']
        if not firmware:
            raise ValidationError("Firmware is required for reassignment.")

        # Ensure the hardware type is set
        if not self.hardware_type:
            raise ValidationError("Hardware type is not defined in the form.")

        # Ensure the firmware is valid for the hardware type
        if firmware.kind != self.hardware_type:
            raise ValidationError(
                f"The selected firmware is not compatible with the {self.hardware_type}."
            )

        return cleaned_data
    


class FirmwareDeviceReassignForm(FirmwareReassignMixin, NetBoxModelForm):
    """
    Form for reassigning firmware to devices.
    """
    hardware_type = 'device'
    firmware = DynamicModelChoiceField(
        queryset=Firmware.objects.all(),
        label='Firmware',
        required=True,
        help_text='Select the firmware to be reassigned.',
        query_params={
            'device_type': '$self__device_type',
        },
    )

    class Meta:
        model = FirmwareAssignment
        fields = FirmwareReassignMixin.Meta.fields

class FirmwareModuleReassignForm(FirmwareReassignMixin, NetBoxModelForm):
    hardware_type = 'module'

    firmware = DynamicModelChoiceField(
        queryset=Firmware.objects.all(),
        label='Firmware',
        required=True,
        help_text='Select the firmware to be reassigned.',
        query_params={
            'kind': 'module',
        },
    )
    class Meta:
        model = FirmwareAssignment
        fields = FirmwareReassignMixin.Meta.fields