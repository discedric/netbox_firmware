from dcim.api.views import DeviceViewSet, InventoryItemViewSet, ModuleViewSet
from netbox.api.viewsets import NetBoxModelViewSet
from utilities.query import count_related
from .. import models
from .serializers import (
    FirmwareSerializer, FirmwareAssignmentSerializer
)

class FirmwareViewSet(NetBoxModelViewSet):
    queryset = models.Firmware.objects.all()
    serializer_class = FirmwareSerializer

class FirmwareAssigmentViewSet(NetBoxModelViewSet):
    queryset = models.FirmwareAssignment.objects.all()
    serializer_class = FirmwareAssignmentSerializer