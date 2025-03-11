import strawberry
import strawberry_django
from typing import Annotated
from extras.graphql.mixins import ContactsMixin, ImageAttachmentsMixin
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
    device_type: (
        Annotated["DeviceTypeType", strawberry.lazy("dcim.graphql.types")] | None
    )
    inventoryitem: (
        Annotated["InventoryItemType", strawberry.lazy("dcim.graphql.types")] | None
    )
    