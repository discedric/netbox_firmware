from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.scalars import BigInt
from netbox.graphql.types import (
    NetBoxObjectType,
    OrganizationalObjectType,
)
from netbox_firmware.models import (
    Firmware,
    FirmwareAssignment,
    Bios,
    BiosAssignment
)
from .filters import (
    FirmwareFilter,
    FirmwareAssignmentFilter,
    BiosFilter,
    BiosAssignmentFilter
)

@strawberry_django.type(Firmware, fields='__all__', filters=FirmwareFilter)
class FirmwareType(NetBoxObjectType):
    manufacturer: Annotated["ManufacturerType", strawberry.lazy('dcim.graphql.types')]
    device_type: List[Annotated["DeviceTypeType", strawberry.lazy("dcim.graphql.types")]] | None
    module_type: List[Annotated["ModuleTypeType", strawberry.lazy('dcim.graphql.types')]] | None

@strawberry_django.type(FirmwareAssignment, fields='__all__', filters=FirmwareAssignmentFilter)
class FirmwareAssignmentType(NetBoxObjectType):
    firmware: Annotated["FirmwareType", strawberry.lazy("netbox_firmware.graphql.types")]
    module: Annotated["ModuleType", strawberry.lazy('dcim.graphql.types')] | None
    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')] | None

@strawberry_django.type(Bios, fields='__all__', filters=BiosFilter)
class BiosType(NetBoxObjectType):
    manufacturer: Annotated["ManufacturerType", strawberry.lazy('dcim.graphql.types')]
    device_type: List[Annotated["DeviceTypeType", strawberry.lazy("dcim.graphql.types")]] | None
    module_type: List[Annotated["ModuleTypeType", strawberry.lazy('dcim.graphql.types')]] | None

@strawberry_django.type(BiosAssignment, fields='__all__', filters=BiosAssignmentFilter)
class BiosAssignmentType(NetBoxObjectType):
    bios: Annotated["BiosType", strawberry.lazy("netbox_firmware.graphql.types")]
    module: Annotated["ModuleType", strawberry.lazy('dcim.graphql.types')] | None
    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')] | None