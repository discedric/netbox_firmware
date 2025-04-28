import strawberry
import strawberry_django

from netbox_firmware.models import (
    Firmware,
    FirmwareAssignment,
)
from .types import (
    FirmwareType,
    FirmwareAssignmentType,
)

@strawberry.type
class FirmwareQuery:
    @strawberry.field
    def firmware(self, info, id: int) -> FirmwareType:
        return Firmware.objects.get(pk=id)
    firmware_list: list[FirmwareType] = strawberry_django.field()

@strawberry.type
class FirmwareAssignmentQuery:
    @strawberry.field
    def firmware_assignment(self, info, id: int) -> FirmwareAssignmentType:
        return FirmwareAssignment.objects.get(pk=id)
    firmware_assignment_list: list[FirmwareAssignmentType] = strawberry_django.field()