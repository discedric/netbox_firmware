from netbox.api.viewsets import NetBoxModelViewSet
from .. import models
from .. import filtersets
from .serializers import (
    FirmwareSerializer, FirmwareAssignmentSerializer
)
"""
    Let op wanneer je een view aanmaakt.
    Je moet een filterset meegeven als je query_params wilt gebruiken. (idioot)
"""

class FirmwareViewSet(NetBoxModelViewSet):
    queryset = models.Firmware.objects.all()
    serializer_class = FirmwareSerializer
    filterset_class = filtersets.FirmwareFilterSet

class FirmwareAssigmentViewSet(NetBoxModelViewSet):
    queryset = models.FirmwareAssignment.objects.all()
    serializer_class = FirmwareAssignmentSerializer
    filterset_class = filtersets.FirmwareAssignmentFilterSet