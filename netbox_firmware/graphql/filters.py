import strawberry_django

from netbox.graphql.filter_mixins import BaseFilterMixin

from netbox_firmware import filtersets, models

__all__ = (
    'FirmwareFilter',
    'FirmwareAssignmentFilter',
)

@strawberry_django.filter(models.Firmware, lookups=True)
class FirmwareFilter(BaseFilterMixin):
    pass

@strawberry_django.filter(models.FirmwareAssignment, lookups=True)
class FirmwareAssignmentFilter(BaseFilterMixin):
    pass

@strawberry_django.filter(models.Bios, lookups=True)
class BiosFilter(BaseFilterMixin):
    pass

@strawberry_django.filter(models.BiosAssignment, lookups=True)
class BiosAssignmentFilter(BaseFilterMixin):
    pass