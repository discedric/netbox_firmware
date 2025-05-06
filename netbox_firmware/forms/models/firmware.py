from dcim.models import DeviceType, Manufacturer, ModuleType, Device, Module
from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
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
    description = forms.CharField(
        required=False,
    )
    file_name = forms.CharField(required=False, label='File Name')
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
        label='Supported Device Type',
    )
    module_type = DynamicModelChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        selector=True,
        label='Module Type',
    )
    comments = CommentField()
    
    fieldsets=(
        FieldSet('name', 'file_name', 'file', 'status', 'description',name='General'),
        FieldSet(
            'manufacturer',
            TabbedGroups(
                FieldSet('device_type',name='Device Type'),
                FieldSet('module_type',name='Module Type'),
            ),
            name='Hardware'
        ),
    )

    class Meta:
        model = Firmware
        fields = [
            'name',
            'file_name',
            'file',
            'description',
            'device_type',
            'module_type',
            'status',
            'comments',
        ]
        widgets = {
            'file': ClearableFileInput(attrs={
                'accept': '.bin,.img,.tar,.tar.gz,.zip,.exe'
                }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields_by_tags()
        # Used for picking the default active tab for hardware type selection
        self.no_hardware_type = True
        if self.instance:
            if (
                self.instance.device_type
                or self.instance.module_type
            ):
                self.no_hardware_type = False

    def clean(self):
        super().clean()
        device_type = self.cleaned_data.get('device_type')
        module_type = self.cleaned_data.get('module_type')

        if device_type and module_type:
            raise forms.ValidationError("You may only select one of 'Device Type' or 'Module Type', not both.")
        
        pass
      
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