import django_filters
from django.db.models import Q
from utilities.filters import (
    ContentTypeFilter, MultiValueCharFilter, MultiValueMACAddressFilter, MultiValueNumberFilter, MultiValueWWNFilter,
    NumericArrayFilter, TreeNodeMultipleChoiceFilter
)
from django.utils.translation import gettext as _
from dcim.models import DeviceType, Manufacturer, ModuleType, Module, Device
from netbox_firmware.choices import BiosStatusChoices, HardwareKindChoices

from netbox.filtersets import NetBoxModelFilterSet
from ..models import Bios, BiosAssignment

class BiosFilterSet(NetBoxModelFilterSet):
    name = MultiValueCharFilter(
        lookup_expr='iexact',
    )
    file_name = MultiValueCharFilter(
        lookup_expr='icontains',
        label=_('File name'),
    )
    status = django_filters.MultipleChoiceFilter(
        choices=BiosStatusChoices,
        label=_('Status'),
    )
    kind = MultiValueCharFilter(
        method='filter_kind',
        label='Type of hardware',
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
    
    class Meta:
        model = Bios
        fields = {
            'id', 'name', 'file_name', 'status',
            'device_type', 'module_type',
        }
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value.strip()) |
            Q(comments__icontains=value) |
            Q(device_type__slug__icontains=value) |
            Q(module_type__model__icontains=value) |
            Q(device_type__manufacturer__slug__icontains=value) |
            Q(module_type__manufacturer__slug__icontains=value)
        ).distinct()

    def filter_kind(self, queryset, name, value):
        query = None
        for kind in HardwareKindChoices.values():
            if kind in value:
                q = Q(**{f'{kind}_type__isnull': False})
                if query:
                    query = query | q
                else:
                    query = q
        if query:
            return queryset.filter(query)
        else:
            return queryset


class BiosAssignmentFilterSet(NetBoxModelFilterSet):
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
    bios = django_filters.ModelMultipleChoiceFilter(
        field_name='bios__name',
        queryset=Bios.objects.all(),
        to_field_name='name',
        label=_('Bios'),
    )
    bios_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Bios.objects.all(),
        label=_('Bios (ID)'),
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
    kind = MultiValueCharFilter(
        method='filter_kind',
        label='Type of hardware',
    )
    module_device = django_filters.ModelMultipleChoiceFilter(
        queryset=Module.objects.all(),
        field_name='module__device',
        label=_('Module (device)'),
    )
    module_sn = django_filters.ModelMultipleChoiceFilter(
        queryset=Module.objects.all(),
        field_name='module__serial',
        label=_('Module (serial)'),
    )
    device_sn = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        field_name='device__serial',
        label=_('Device (serial)'),
    )
    
    class Meta:
        model = BiosAssignment
        fields = {
            'id', 'description', 'ticket_number', 'patch_date', 'comment',
            'bios', 'device', 
            'module',
        }
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(description__icontains=value) |
            Q(ticket_number__icontains=value) |
            Q(comment__icontains=value) |
            Q(bios__name__icontains=value) |
            Q(device__device_type__slug__icontains=value) |
            Q(module__module_type__model__icontains=value) |
            Q(device__name__icontains=value) |
            Q(device__serial__icontains=value) |
            Q(module__serial__icontains=value)
        ).distinct()

    def filter_kind(self, queryset, name, value):
        query = None
        for kind in HardwareKindChoices.values():
            if kind in value:
                q = Q(**{f'{kind}__isnull': False})
                if query:
                    query = query | q
                else:
                    query = q
        if query:
            return queryset.filter(query)
        else:
            return queryset