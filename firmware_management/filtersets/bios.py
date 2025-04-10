import django_filters
from django.db.models import Q
from utilities.filters import (
    ContentTypeFilter, MultiValueCharFilter, MultiValueMACAddressFilter, MultiValueNumberFilter, MultiValueWWNFilter,
    NumericArrayFilter, TreeNodeMultipleChoiceFilter,
)
from django.utils.translation import gettext as _
from dcim.models import DeviceType, Manufacturer, ModuleType
from dcim.choices import DeviceStatusChoices
from netbox.filtersets import NetBoxModelFilterSet
from ..models import Bios, BiosAssignment
from .. import choices

class BiosFilterSet(NetBoxModelFilterSet):
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
            Q(comments__icontains=value) 
        ).distinct()


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
    device = MultiValueCharFilter(
        lookup_expr='icontains',
    )
    module = MultiValueCharFilter(
        lookup_expr='icontains',
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
            Q(comment__icontains=value)
        ).distinct()