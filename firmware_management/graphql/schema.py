import strawberry
import strawberry_django

from firmware_management.models import (
    Firmware,
    FirmwareAssignment,
    InventoryItemType,
)
from .types import (
    FirmwareType,
    FirmwareAssignmentType,
)

@strawberry.type
class FirmwareQuery:
    @strawberry.field
    def firmware(self, info, id: int, **kwargs):
        if id:
            return Firmware.objects.get(id=id)
        return Firmware.objects.all()

@strawberry.type
class FirmwareAssignmentQuery:
    @strawberry.field
    def firmware_assignment(self, info, id: int, **kwargs):
        if id:
            return FirmwareAssignment.objects.get(id=id)
        return FirmwareAssignment.objects.all()