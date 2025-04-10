from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.scalars import BigInt
from netbox.graphql.types import (
    NetBoxObjectType,
    OrganizationalObjectType,
)
from firmware_management.models import (
    Firmware,
    FirmwareAssignment,
)
from .filters import (
    FirmwareFilter,
    FirmwareAssignmentFilter,
)

@strawberry_django.type(Firmware, fields='__all__', filters=FirmwareFilter)
class FirmwareType(NetBoxObjectType):
    manufacturer: Annotated["ManufacturerType", strawberry.lazy('dcim.graphql.types')]
    device_type: Annotated["DeviceTypeType", strawberry.lazy("dcim.graphql.types")] | None
    module_type: List[Annotated["ModuleTypeType", strawberry.lazy('dcim.graphql.types')]] | None

@strawberry_django.type(FirmwareAssignment, fields='__all__', filters=FirmwareAssignmentFilter)
class FirmwareAssignmentType(NetBoxObjectType):
    firmware: Annotated["FirmwareType", strawberry.lazy("firmware_management.graphql.types")]
    manufacturer: Annotated["ManufacturerType", strawberry.lazy('dcim.graphql.types')]
    device_type: Annotated["DeviceTypeType", strawberry.lazy("dcim.graphql.types")] | None
    module_type: List[Annotated["ModuleTypeType", strawberry.lazy('dcim.graphql.types')]] | None
    module: Annotated["ModuleType", strawberry.lazy('dcim.graphql.types')] | None
    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')] | None
    inventory_item: Annotated["InventoryItemType", strawberry.lazy('dcim.graphql.types')] | None
    