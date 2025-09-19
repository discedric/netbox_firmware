from dcim.models import DeviceType, Manufacturer, ModuleType, Device, Module
from django import forms
from django.core.exceptions import ValidationError
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms.widgets import DatePicker, ClearableFileInput
from netbox_firmware.utils import get_tags_and_edit_protected_firmware_fields
from netbox_firmware.filtersets import FirmwareFilterSet, FirmwareAssignmentFilterSet
from netbox_firmware.models import Firmware, FirmwareAssignment

__all__ = (
    'FirmwareForm',
    'FirmwareAssignmentForm',
)

class FirmwareForm(NetBoxModelForm):
    name = forms.CharField()
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="Manufacturer",
        selector=True,
        quick_add=True
    )
    description = forms.CharField(
        required=False,
    )
    file_name = forms.CharField(required=False, label='File Name')
    device_type = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        query_params={
            'manufacturer_id': '$manufacturer',
        },
        required=False,
        selector=True,
        label='Supported Device Type',
    )
    module_type = DynamicModelMultipleChoiceField(
        queryset=ModuleType.objects.all(),
        query_params={
            'manufacturer_id': '$manufacturer',
        },
        required=False,
        selector=True,
        label='Supported Module Type',
    )
    comments = CommentField()
    
    fieldsets=(
        FieldSet('name', 'manufacturer', 'file_name', 'file', 'status', 'description',name='General'),
        FieldSet(
            TabbedGroups(
                FieldSet('device_type',name='Device Type'),
                FieldSet('module_type',name='Module Type')
            ),
            name='Hardware'
        ),
    )

    class Meta:
        model = Firmware
        fields = '__all__'
        widgets = {
            'file': ClearableFileInput(attrs={
                'accept': '.bin,.img,.tar,.tar.gz,.zip,.exe'
                }),
        }


    ### This checks what type is assigned to the firmware and will filter the template to show only one the type used.
    ### IT will also grey out the Manufacturer field once a Device Type or Module Type is assigned.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default: assume no hardware type selected
        self.no_hardware_type = True

        if self.instance and self.instance.pk:
            has_device_type = self.instance.device_type.exists()
            has_module_type = self.instance.module_type.exists()

            if has_device_type or has_module_type:
                # Used for template logic (which tab to show)
                self.no_hardware_type = False

                # Disable manufacturer field once firmware is linked
                self.fields['manufacturer'].disabled = True


    def clean(self):
        return super().clean()
      
class FirmwareAssignmentForm(NetBoxModelForm):
    # Hardware ------------------------------
    description = forms.CharField(
        required=False,
    )

    # Hardware Items ------------------------
    device = DynamicModelChoiceField(
        queryset = Device.objects.all(),
        required=False,
        selector=True,
        label='Device',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    module = DynamicModelChoiceField(
        queryset = Module.objects.all(),
        required=False,
        selector=True,
        label='Module',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    
    # Update --------------------------------
    firmware = DynamicModelChoiceField(
        queryset=Firmware.objects.all(),
        selector=True,
        required=True,
        label='Firmware',
        help_text='Only showing Active and Staged',
        query_params={
            'status__in': ['active','staged'],
            'device': '$device',
            'module': '$module',
        },
    )
    comment = CommentField()
    
    fieldsets = (
        FieldSet(
            'description',
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
    
    class Meta:
        model = FirmwareAssignment
        fields = [
            'description',
            'ticket_number',
            'patch_date',
            'comment',
            'firmware',
            'device',
            'module',
        ]
        widgets = {
            'patch_date': DatePicker(),
        }
    
    def clean(self):
        super().clean()
        device = self.cleaned_data.get('device')
        module = self.cleaned_data.get('module')

        if device and module:
            raise forms.ValidationError("You may only select one of 'Device' or 'Module', not both.")
        
        pass