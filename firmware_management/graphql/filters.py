import strawberry_django

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

from firmware_management import filtersets, models

__all__ = (
    'FirmwareFilter',
    'FirmwareAssignmentFilter',
)

@strawberry_django.filter(models.Firmware, lookups=True)
@autotype_decorator(filtersets.FirmwareFilterSet)
class FirmwareFilter(BaseFilterMixin):
    pass

@strawberry_django.filter(models.FirmwareAssignment, lookups=True)
@autotype_decorator(filtersets.FirmwareAssignmentFilterSet)
class FirmwareAssignmentFilter(BaseFilterMixin):
    pass