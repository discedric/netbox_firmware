import strawberry
import strawberry_django

from netbox_firmware.models import (
    Firmware,
    FirmwareAssignment,
    Bios,
    BiosAssignment,
)
from .types import (
    FirmwareType,
    FirmwareAssignmentType,
    BiosType,
    BiosAssignmentType,
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

@strawberry.type
class BiosQuery:
    @strawberry.field
    def bios(self, info, id: int) -> BiosType:
        return Bios.objects.get(pk=id)
    bios_list: list[BiosType] = strawberry_django.field()

@strawberry.type
class BiosAssignmentQuery:
    @strawberry.field
    def bios_assignment(self, info, id: int) -> BiosAssignmentType:
        return BiosAssignment.objects.get(pk=id)
    bios_assignment_list: list[BiosAssignmentType] = strawberry_django.field()