from functools import reduce
from django.db.models import Q
import django_filters

from dcim.filtersets import DeviceFilterSet, InventoryItemFilterSet, ModuleFilterSet
from dcim.models import Manufacturer, Device, DeviceType, DeviceRole, Module, ModuleType, InventoryItem, InventoryItemRole, Rack, RackRole, RackType, Site, Location
from netbox.filtersets import NetBoxModelFilterSet
from utilities import filters
from .choices import HardwareKindChoices, FirmwareStatusChoices
from .models import Firmware, FirmwareAssignment, InventoryItemType
from .utils import query_located, get_firmware_custom_fields_search_filters

class FirmwareFilterSet(NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=FirmwareStatusChoices,
    )
    kind = filters.MultiValueCharFilter(
        method='filter_kind',
        label='Type of hardware',
    )
    manufacturer_id = filters.MultiValueCharFilter(
        method='filter_manufacturer',
        label='Manufacturer (ID)',
    )
    manufacturer_name = filters.MultiValueCharFilter(
        method='filter_manufacturer',
        label='Manufacturer (name)',
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type',
        queryset=DeviceType.objects.all(),
        label='Device type (ID)',
    )
    device_type = filters.MultiValueCharFilter(
        field_name='device_type__slug',
        lookup_expr='iexact',
        label='Device type (slug)',
    )
    device_type_model = filters.MultiValueCharFilter(
        field_name='device_type__model',
        lookup_expr='icontains',
        label='Device type (model)',
    )
    inventory_item_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='inventory_item_type',
        queryset=InventoryItemType.objects.all(),
        label='Inventory item type (ID)',
    )
    inventory_item_type = filters.MultiValueCharFilter(
        field_name='inventory_item_type__slug',
        lookup_expr='iexact',
        label='Inventory item type (slug)',
    )
    inventory_item_type_model = filters.MultiValueCharFilter(
        field_name='inventory_item_type__model',
        lookup_expr='icontains',
        label='Inventory item type (model)',
    )

    class Meta:
        model = Firmware
        fields = ('id', 'name', 'device_type', 'manufacturer','file_name')

    def search(self, queryset, name, value):
        query = (
            Q(id__contains=value)
            | Q(serial__icontains=value)
            | Q(name__icontains=value)
            | Q(firmware_tag__icontains=value)
            | Q(device_type__model__icontains=value)
            | Q(inventory_item_type__model__icontains=value)
            | Q(device__name__icontains=value)
            | Q(inventory_item__name__icontains=value)
        )
        custom_field_filters = get_firmware_custom_fields_search_filters()
        for custom_field_filter in custom_field_filters:
            query |= Q(**{custom_field_filter: value})

        return queryset.filter(query)

    def filter_kind(self, queryset, name, value):
        query = None
        for kind in HardwareKindChoices.values():
            if kind in value:
                q = Q(**{f'{kind}_type__isnull':False})
                if query:
                    query = query|q
                else:
                    query = q
        if query:
            return queryset.filter(query)
        else:
            return queryset

    def filter_manufacturer(self, queryset, name, value):
        if name == 'manufacturer_id':
            return queryset.filter(
                Q(device_type__manufacturer__in=value)|
                Q(module_type__manufacturer__in=value)|
                Q(inventoryitem_type__manufacturer__in=value)
            )
        elif name == 'manufacturer_name':
            # OR for every passed value and for all hardware types
            q = Q()
            for v in value:
                q |= Q(device_type__manufacturer__name__icontains=v)
                q |= Q(module_type__manufacturer__name__icontains=v)
                q |= Q(inventoryitem_type__manufacturer__name__icontains=v)
            return queryset.filter(q)

    def filter_located(self, queryset, name, value):
        return query_located(queryset, name, value)