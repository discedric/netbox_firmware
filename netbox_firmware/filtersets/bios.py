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
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer__name',
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label=_('Manufacturer (Name)'),
    )
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer (ID)'),
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type__model',
        queryset=DeviceType.objects.all(),
        to_field_name='model',
        label=_('Device type (Model)'),
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type',
        queryset=DeviceType.objects.all(),
        label=_('Device type (ID)'),
    )
    device = django_filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        method='filter_by_device',
        label=_('Device'),
    )
    module_type = django_filters.ModelMultipleChoiceFilter(
        field_name='module_type__model',
        queryset=ModuleType.objects.all(),
        to_field_name='model',
        label=_('Module type (Model)'),
    )
    module_type_id = django_filters.ModelMultipleChoiceFilter(
        field_name='module_type',
        queryset=ModuleType.objects.all(),
        label=_('Module type (ID)'),
    )
    module = django_filters.ModelChoiceFilter(
        queryset=Module.objects.all(),
        method='filter_by_module',
        label=_('Module'),
    )

    ## In the class Meta you can only add field names that are actual fields of the model.
    class Meta:
        model = Bios
        fields = {
            'id', 'name', 'file_name', 'status',
            'device_type', 'module_type',
        }
    
    ### Criteria for the Quick search box.
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(manufacturer__name__icontains=value) |
            Q(device_type__model__icontains=value) |
            Q(module_type__model__icontains=value) 
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

    ### Filter needed to show only the compatible firmwares for a device during assignment
    def filter_by_device(self, queryset, name, value):
        return queryset.filter(device_type=value.device_type)

    ### Filter needed to show only the compatible firmwares for a module during assignment
    def filter_by_module(self, queryset, name, value):
        return queryset.filter(module_type=value.module_type)

    # def filter_by_manufacturer(self, queryset, name, value):
    #     if value:
    #         return queryset.filter(
    #             Q(device_type__manufacturer__in=value) |
    #             Q(module_type__manufacturer__in=value)
    #         ).distinct()
    #     return queryset

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
    kind = MultiValueCharFilter(
        method='filter_kind',
        label='Type of hardware',
    )
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Manufacturer.objects.all(),
        label=_('Manufacturer (ID)'),
        method='filter_by_manufacturer',  # Custom filter method
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        queryset=DeviceType.objects.all(),
        field_name='device__device_type__model',
        to_field_name='model',
        label=_('Device type (model)'),
    )
    device_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=DeviceType.objects.all(),
        field_name='device__device_type',
        label=_('Device type (ID)'),
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
    device_sn = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        field_name='device__serial',
        label=_('Device Serial Number'),
    )
    module_type = django_filters.ModelMultipleChoiceFilter(
        queryset=ModuleType.objects.all(),
        field_name='module__module_type__model',
        to_field_name='model',
        label=_('Module type (model)'),
    )
    module_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ModuleType.objects.all(),
        field_name='module__module_type',
        label=_('Module type (ID)'),
    )
    module_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Module.objects.all(),
        label=_('Module (ID)'),
    )
    module_sn = django_filters.CharFilter(
        field_name='module__serial',
        lookup_expr='icontains',
        label=_('Module Serial Number'),
    )
    module_device = django_filters.ModelMultipleChoiceFilter(
        queryset=Module.objects.all(),
        field_name='module__device',
        label=_('Module (device)'),
    )
    module_device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        field_name='module__device_id',
        label=_('Module (device ID)'),
    )



    ## In the class Meta you can only add field names that are actual fields of the model.
    class Meta:
        model = BiosAssignment
        fields = {
            'id', 'description', 'ticket_number', 'patch_date', 'comment',
            'bios', 'device', 'module',
        }
    
    ### Criteria for the Quick search box.
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(description__icontains=value) |
            Q(ticket_number__icontains=value) |
            Q(comment__icontains=value) |
            Q(bios__name__icontains=value) |
            Q(device__device_type__model__icontains=value) |
            Q(module__module_type__model__icontains=value) |
            Q(device__name__icontains=value) |
            Q(device__serial__icontains=value) |
            Q(module__serial__icontains=value) |
            Q(device__device_type__manufacturer__name__icontains=value) |
            Q(module__module_type__manufacturer__name__icontains=value) 
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
    
    ### Custom filter to filter by manufacturer, checking both device and module manufacturer
    def filter_by_manufacturer(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(device__device_type__manufacturer__in=value) |
                Q(module__module_type__manufacturer__in=value)
            ).distinct()
        return queryset