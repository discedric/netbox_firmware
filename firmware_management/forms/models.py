from dcim.models import DeviceType, Manufacturer, InventoryItem, ModuleType, Location, RackType, Site
from netbox_inventory.models import InventoryItemType
from django import forms
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
    name = forms.CharField()
    file_name = forms.CharField(required=False, label='File Name')
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label='Manufacturer',
        initial_params={
            'device_types': '$device_type',
            'inventoryitem_types': '$inventory_item_type',
        },
    )
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        label='Supported Device Type',
        initial_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    inventory_item_type = DynamicModelChoiceField(
        queryset=InventoryItemType.objects.all(),
        required=False,
        initial_params={
           'manufacturer_id': '$manufacturer',
        },
        label='Inventory Item Type',
    )
    comments = CommentField()
    
    fieldsets=(
        FieldSet('name', 'file_name','status','comments',name='General'),
        FieldSet('manufacturer','device_type','inventory_item_type',name='Hardware'),
    )

    class Meta:
        model = Firmware
        fields = [
            'name',
            'file_name',
            'manufacturer',
            'device_type',
            'inventory_item_type',
            'status',
            'comments',
        ]
    
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