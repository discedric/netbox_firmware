from dcim.models import DeviceType, Manufacturer, ModuleType, InventoryItem, Device, Module
from netbox_inventory.models import InventoryItemType
from django import forms
from netbox.forms import NetBoxModelForm
from netbox_inventory.choices import HardwareKindChoices
from utilities.forms.fields import CommentField, DynamicModelChoiceField, SlugField
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms.widgets import DatePicker
from ..utils import get_tags_and_edit_protected_firmware_fields
from ..models import Firmware, FirmwareAssignment

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
    
    fieldsets=(
        FieldSet('name', 'file_name','status', 'description',name='General'),
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

    class Meta:
        model = Firmware
        fields = [
            'name',
            'file_name',
            'description',
            'manufacturer',
            'device_type',
            'module_type',
            'inventory_item_type',
            'status',
            'comments',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields_by_tags()
        # Used for picking the default active tab for hardware type selection
        self.no_hardware_type = True
        if self.instance:
            if (
                self.instance.device_type
                or self.instance.module_type
                or self.instance.inventory_item_type
            ):
                self.no_hardware_type = False
    
    def _disable_fields_by_tags(self):
        """
        We need to disable fields that are not editable based on the tags that are assigned to the firmware.
        """
        if not self.instance.pk:
            # If we are creating a new firmware we can't disable fields
            return

        # Disable fields that should not be edited
        tags = self.instance.tags.all().values_list('slug', flat=True)
        tags_and_disabled_fields = get_tags_and_edit_protected_firmware_fields()

        for tag in tags:
            if tag not in tags_and_disabled_fields:
                continue

            for field in tags_and_disabled_fields[tag]:
                if field in self.fields:
                    self.fields[field].disabled = True
    
    
class FirmwareAssignmentForm(NetBoxModelForm):
    # Hardware ------------------------------
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        selector=True,
        required=True,
        label='Manufacturer',
        initial_params={
            'device_types': '$device_type',
            'module_types': '$module_type',
            'inventory_item_types': '$inventory_item_type',
        },
    )
    description = CommentField()
    
    device = DynamicModelChoiceField(
        queryset = Device.objects.all(),
        required=False,
        selector=True,
        label='Device',
        query_params={
            'manufacturer_id': '$manufacturer',
            'device_type_id': '$device_type',
        },
        context={
            'parent': 'device',
        }
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
        context={
            'parent': 'module',
        }
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
        context={
            'parent': 'inventory_item',
        }
    )
    
    # Hardware Type -------------------------
    supported_device = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        selector=True,
        label='Supported Device Type',
        context={
            'parent': 'device_type',
        },
        query_params={
           'manufacturer_id': '$manufacturer',
        },
    )
    module_type = DynamicModelChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        selector=True,
        label='Supported Netbox Inventory Item Type',
        context={
            'parent': 'module_type',
        },
        query_params={
           'manufacturer_id': '$manufacturer',
        },
    )
    item_type = DynamicModelChoiceField(
        queryset=InventoryItemType.objects.all(),
        required=False,
        selector=True,
        label='Supported Netbox Inventory Item Type',
        context={
            'parent': 'inventory_item_type',
        },
        query_params={
           'manufacturer_id': '$manufacturer',
        },
    )
    
    # Update --------------------------------
    firmware = DynamicModelChoiceField(
        queryset=Firmware.objects.all(),
        #selector=True,  -> moeten we een filterform voor maken, doen we later wel
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
    
    
    fieldsets = (
        FieldSet(
            'manufacturer',
            TabbedGroups(
                FieldSet('supported_device',name='Device Type'),
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