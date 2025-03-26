from django import forms

from dcim.models import DeviceType, Manufacturer, ModuleType, InventoryItem, Device, Module
from netbox_inventory.models import InventoryItemType
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
)
from utilities.forms.rendering import FieldSet, TabbedGroups

from ..choices import FirmwareStatusChoices
from ..models import (
    Firmware,
    FirmwareAssignment
)
from ..utils import get_plugin_setting

class FirmwareBulkEditForm(NetBoxModelBulkEditForm):
    name = forms.CharField()
    description = forms.CharField(
        required=False,
    )
    file_name = forms.CharField(required=False, label='File Name')
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label='Manufacturer',
        selector=True,
        quick_add=True,
        initial_params={
            'device_types': '$device_type',
            'inventory_item_types': '$inventory_item_type',
        },
    )
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
        label='Supported Device Type',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    module_type = DynamicModelChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        selector=True,
        label='Module Type',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    inventory_item_type = DynamicModelChoiceField(
        queryset=InventoryItemType.objects.all(),
        required=False,
        selector=True,
        query_params={
           'manufacturer_id': '$manufacturer',
        },
        label='Inventory Item Type',
    )
    comments = CommentField()
    
    model = Firmware
    fieldsets=(
        FieldSet('name', 'file_name', 'file', 'status', 'description',name='General'),
        FieldSet(
            'manufacturer',
            TabbedGroups(
                FieldSet('device_type',name='Device Type'),
                FieldSet('module_type',name='Module Type'),
                FieldSet('inventory_item_type',name='Inventory Item Type'),
            ),
            name='Hardware'
        ),
    )
    

class FirmwareAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        selector=True,
        required=True,
        label='Manufacturer',
        initial_params={
            'device_types': '$device_type',
            'module_types': '$module_type',
            'inventory_item_types': '$inventory_item_type',
            'firmware': '$firmware',
        },
    )
    description = CommentField()
    
    # Hardware Type -------------------------
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
        label='Supported Device Type',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    module_type = DynamicModelChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        selector=True,
        label='Supported Netbox Inventory Item Type',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    item_type = DynamicModelChoiceField(
        queryset=InventoryItemType.objects.all(),
        required=False,
        selector=True,
        label='Supported Netbox Inventory Item Type',
        query_params={
            'manufacturer_id': '$manufacturer',
        },
    )
    
    # Hardware Items ------------------------
    
    device = DynamicModelChoiceField(
        queryset = Device.objects.all(),
        required=False,
        selector=True,
        label='Device',
        query_params={
            'manufacturer_id': '$manufacturer',
            'device_type_id': '$device_type',
        },
    )
    module = DynamicModelChoiceField(
        queryset = Module.objects.all(),
        required=False,
        selector=True,
        label='Module',
        query_params={
            'manufacturer_id': '$manufacturer',
            'module_type_id': '$module_type',
        },
    )
    inventory_item = DynamicModelChoiceField(
        queryset = InventoryItem.objects.all(),
        required=False,
        selector=True,
        label='Inventory Item',
        query_params={
            'manufacturer_id': '$manufacturer',
            'inventory_item_type_id': '$inventory_item_type',
        },
    )
    
    # Update --------------------------------
    firmware = DynamicModelChoiceField(
        queryset=Firmware.objects.all(),
        selector=True,
        required=True,
        label='Firmware',
        query_params={
            'manufacturer_id': '$manufacturer',
            'device_type_id': '$device_type',
            'module_type_id': '$module_type',
            'inventory_item_type_id': '$inventory_item_type',
        },
    )
    comment = CommentField()
    
    model= FirmwareAssignment
    fieldsets = (
        FieldSet(
            'manufacturer',
            TabbedGroups(
                FieldSet('device_type',name='Device Type'),
                FieldSet('module_type',name='Module Type'),
                FieldSet('item_type',name='Inventory Item Type'),
            ),
            TabbedGroups(
                FieldSet('device',name='Device'),
                FieldSet('module',name='Module'),
                FieldSet('inventory_item',name='Inventory Item'),
            ),
            name='Hardware'
        ),
        FieldSet(
            'firmware','patch_date','comment',
            name='Update'
        ),
        FieldSet(
            'ticket_number',
            name='General'
        ),
    )
    nullable_fields = ['device_type', 'module_type', 'item_type', 'device', 'module', 'inventory_item', 'ticket_number', 'patch_date', 'comment']