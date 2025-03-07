from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from firmware_management.models import Firmware, FirmwareAssignment


class FirmwareSerializer(NetBoxModelSerializer):
    class Meta:
        model = Firmware
        fields = '__all__'


class FirmwareAssignmentSerializer(NetBoxModelSerializer):
    firmware = FirmwareSerializer(read_only=True)
    class Meta:
        model = FirmwareAssignment
        fields = '__all__'