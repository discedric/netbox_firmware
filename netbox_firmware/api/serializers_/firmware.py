from netbox.api.serializers import NetBoxModelSerializer
from dcim.api.serializers import DeviceTypeSerializer, ManufacturerSerializer, ModuleTypeSerializer
from netbox_firmware.models import Firmware, FirmwareAssignment


class FirmwareSerializer(NetBoxModelSerializer):
    class Meta:
        model = Firmware
        fields = '__all__'


class FirmwareAssignmentSerializer(NetBoxModelSerializer):
    firmware = FirmwareSerializer(nested=True, required=True)
    class Meta:
        model = FirmwareAssignment
        fields = '__all__'