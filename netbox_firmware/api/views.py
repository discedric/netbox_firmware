from netbox.api.viewsets import NetBoxModelViewSet
from .. import models
from .. import filtersets
from .serializers import (
    FirmwareSerializer, FirmwareAssignmentSerializer, BiosSerializer, BiosAssignmentSerializer
)

class FirmwareViewSet(NetBoxModelViewSet):
    queryset = models.Firmware.objects.all()
    serializer_class = FirmwareSerializer
    filterset_class = filtersets.FirmwareFilterSet

class FirmwareAssigmentViewSet(NetBoxModelViewSet):
    queryset = models.FirmwareAssignment.objects.all()
    serializer_class = FirmwareAssignmentSerializer
    filterset_class = filtersets.FirmwareAssignmentFilterSet
    
class BiosViewSet(NetBoxModelViewSet):
    queryset = models.Bios.objects.all()
    serializer_class = BiosSerializer
    filterset_class = filtersets.BiosFilterSet
    
class BiosAssigmentViewSet(NetBoxModelViewSet):
    queryset = models.BiosAssignment.objects.all()
    serializer_class = BiosAssignmentSerializer
    filterset_class = filtersets.BiosAssignmentFilterSet