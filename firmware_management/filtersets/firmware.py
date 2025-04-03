import django_filters
from django.db.models import Q
from utilities.filters import (
    ContentTypeFilter, MultiValueCharFilter, MultiValueMACAddressFilter, MultiValueNumberFilter, MultiValueWWNFilter,
    NumericArrayFilter, TreeNodeMultipleChoiceFilter,
)
from django.utils.translation import gettext as _
from dcim.models import DeviceType, Manufacturer, ModuleType, Device, InventoryItem, Module
from dcim.choices import DeviceStatusChoices
from netbox_inventory.models import InventoryItemType
from netbox.filtersets import NetBoxModelFilterSet
from ..models import Firmware, FirmwareAssignment
from .. import choices


class FirmwareFilterSet(NetBoxModelFilterSet):
    name = MultiValueCharFilter(
        lookup_expr='iexact',
    )
    file_name = MultiValueCharFilter(
        lookup_expr='icontains',
        label=_('File name'),
    )
    status = django_filters.MultipleChoiceFilter(
        choices=DeviceStatusChoices,
        label=_('Status'),
    )
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer',
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer (ID)'),
    )
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer__slug',
        queryset=Manufacturer.objects.all(),
        to_field_name='slug',
        label=_('Manufacturer name (slug)'),
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type__slug',
        queryset=DeviceType.objects.all(),
        to_field_name='slug',
        label=_('Device type name (slug)'),
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type',
        queryset=DeviceType.objects.all(),
        label=_('Device type (ID)'),
    )
    inventory_item_type = django_filters.ModelMultipleChoiceFilter(
        field_name='inventory_item_type__slug',
        queryset=InventoryItemType.objects.all(),
        to_field_name='slug',
        label=_('Inventory item type name (slug)'),
    )
    inventory_item_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=InventoryItemType.objects.all(),
        label=_('Inventory item type (ID)'),
    )
    module_type = django_filters.ModelMultipleChoiceFilter(
        field_name='module_type__model',
        queryset=ModuleType.objects.all(),
        to_field_name='name',
        label=_('Module type (model)'),
    )
    module_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ModuleType.objects.all(),
        label=_('Module type (ID)'),
    )
    
    kind = django_filters.MultipleChoiceFilter(
        choices=choices.HardwareKindChoices,
        method='filter_kind',
        label=_('Hardware kind'),
    )
    
    class Meta:
        model = Firmware
        fields = {
            'id', 'name', 'file_name', 'status',
            'manufacturer', 
            'device_type', 'module_type', 'inventory_item_type',
        }
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value.strip()) |
            Q(comments__icontains=value) 
        ).distinct()
    
    def filter_kind(self, queryset, name, value):
        """
        Dynamically filter the queryset based on which type field is not null.
        """
        # Check which type field is provided in the filter
        device_type = self.data.get('device_type')
        module_type = self.data.get('module_type')
        inventory_item_type = self.data.get('inventory_item_type')

        # Apply filtering based on the provided type
        if device_type:
            return queryset.filter(device_type__isnull=False)
        elif module_type:
            return queryset.filter(module_type__isnull=False)
        elif inventory_item_type:
            return queryset.filter(inventory_item_type__isnull=False)

        # If no specific type is provided, return all firmware objects where any type is not null
        return queryset.filter(
            Q(device_type__isnull=False) |
            Q(module_type__isnull=False) |
            Q(inventory_item_type__isnull=False)
    )


class FirmwareAssignmentFilterSet(NetBoxModelFilterSet):
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer',
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer (ID)'),
    )
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer__slug',
        queryset=Manufacturer.objects.all(),
        to_field_name='slug',
        label=_('Manufacturer (slug)'),
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type__slug',
        queryset=DeviceType.objects.all(),
        to_field_name='slug',
        label=_('Device type (slug)'),
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=DeviceType.objects.all(),
        label=_('Device type (ID)'),
    )
    module_type = django_filters.ModelMultipleChoiceFilter(
        field_name='module_type__model',
        queryset=ModuleType.objects.all(),
        to_field_name='name',
        label=_('Module type (model)'),
    )
    module_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ModuleType.objects.all(),
        label=_('Module type (ID)'),
    )
    inventory_item_type = django_filters.ModelMultipleChoiceFilter(
        field_name='inventory_item_type__slug',
        queryset=InventoryItemType.objects.all(),
        to_field_name='slug',
        label=_('Inventory item type (slug)'),
    )
    inventory_item_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=InventoryItemType.objects.all(),
        label=_('Inventory item type (ID)'),
    )
    description = MultiValueCharFilter(
        lookup_expr='icontains',
    )
    ticket_number = MultiValueCharFilter(
        lookup_expr='icontains',
        label=_('Ticket number'),
    )
    patch_date = django_filters.DateFromToRangeFilter(
        label=_('Patch date'),
    )
    comment = MultiValueCharFilter(
        lookup_expr='icontains',
    )
    firmware = django_filters.ModelMultipleChoiceFilter(
        field_name='firmware__name',
        queryset=Firmware.objects.all(),
        to_field_name='name',
        label=_('Firmware'),
    )
    firmware_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Firmware.objects.all(),
        label=_('Firmware (ID)'),
    )
    device = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        field_name='device__name',
        to_field_name='name',
        label=_('Device (name)'),
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        label=_('Device (ID)'),
    )
    module_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Module.objects.all(),
        label=_('Module (ID)'),
    )
    inventory_item = django_filters.ModelMultipleChoiceFilter(
        queryset=InventoryItem.objects.all(),
        field_name='inventory_item__name',
        to_field_name='name',
        label=_('Inventory Item (name)'),
    )
    inventory_item_id = django_filters.ModelMultipleChoiceFilter(
        queryset=InventoryItem.objects.all(),
        label=_('Inventory Item (ID)'),
    )
    
    
    class Meta:
        model = FirmwareAssignment
        fields = {
            'id', 'description', 'ticket_number', 'patch_date', 'comment',
            'firmware', 'manufacturer', 
            'device_type', 'device', 
            'module_type', 'module',
            'inventory_item', 'inventory_item_type',
        }
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(description__icontains=value) |
            Q(ticket_number__icontains=value) |
            Q(comment__icontains=value)
        ).distinct()