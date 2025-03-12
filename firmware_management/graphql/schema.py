import strawberry
import strawberry_django

from firmware_management.models import (
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
        return Firmware.objects.get(id=id)

@strawberry.type
class FirmwareAssignmentQuery:
    @strawberry.field
    def firmware_assignment(self, info, id: int) -> FirmwareAssignmentType:
        return FirmwareAssignment.objects.get(id=id)