from dcim.models import DeviceType, Manufacturer, InventoryItem, ModuleType, Location, RackType, Site
from netbox_inventory.models import InventoryItemType
from netbox.forms import NetBoxModelForm
from netbox_inventory.choices import HardwareKindChoices
from utilities.forms.fields import CommentField, DynamicModelChoiceField, SlugField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import DatePicker
from tenancy.models import Contact, ContactGroup, Tenant
from ..models import Firmware, FirmwareAssignment

__all__ = (
    'FirmwareForm',
    'FirmwareAssignmentForm',
)

class FirmwareForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label='Manufacturer'
    )
    supported_device = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        label='Supported Device Type'
    )
    
    comment = CommentField()
    
    fieldsets=(
        FieldSet('name','comment',name='General'),
        FieldSet('manufacturer','supported_device','status',name='Hardware'),
    )

    class Meta:
        model = Firmware
        fields = [
            'name',
            'manufacturer',
            'supported_device',
            'status',
            'comment',
        ]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class FirmwareAssignmentForm(NetBoxModelForm):
    firmware = DynamicModelChoiceField(
        queryset=Firmware.objects.all(),
        required=True,
        label='Firmware'
    )
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label='Manufacturer'
    )
    supported_device = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        label='Supported Device Type'
    )
    inventory_item = DynamicModelChoiceField(
        queryset = InventoryItem.objects.all(),
        required=True,
        label='Inventory Item'
    )
    item_type = DynamicModelChoiceField(
        queryset=InventoryItemType.objects.all(),
        required=False,
        label='Supported Netbox Inventory Item Type'
    )
    description = CommentField()
    comment = CommentField()
    
    fieldsets = (
        FieldSet('ticket_number',name='General'),
        FieldSet('manufacturer','inventory_item','device','supported_device',name='Hardware'),
        FieldSet('item_type',name='Netbox Inventory'),
        FieldSet('firmware','patch_date','comment',name='Update'),
    )
    
    class Meta:
        model = FirmwareAssignment
        fields = [
            'description',
            'ticket_number',
            'patch_date',
            'comment',
            'firmware',
            'manufacturer',
            'supported_device',
            'device',
            'inventory_item',
            'item_type'
        ]
        widgets = {
            'patch_date': DatePicker(),
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data