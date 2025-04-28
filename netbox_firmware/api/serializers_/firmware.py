from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers
from dcim.api.serializers import DeviceTypeSerializer, ManufacturerSerializer, ModuleTypeSerializer
from netbox_inventory.api.serializers import InventoryItemTypeSerializer
from netbox_firmware.models import Firmware, FirmwareAssignment


class FirmwareSerializer(NetBoxModelSerializer):
    kind = serializers.SerializerMethodField()
    class Meta:
        model = Firmware
        fields = '__all__'
    def get_kind(self,obj):
        return obj.kind


class FirmwareAssignmentSerializer(NetBoxModelSerializer):
    firmware = FirmwareSerializer(nested=True, required=True)
    class Meta:
        model = FirmwareAssignment
        fields = '__all__'