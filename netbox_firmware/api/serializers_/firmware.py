from netbox.api.serializers import NetBoxModelSerializer
from dcim.api.serializers import ManufacturerSerializer, DeviceTypeSerializer, ModuleTypeSerializer, DeviceSerializer, ModuleSerializer
from netbox_firmware.models import Firmware, FirmwareAssignment

__all__ = (
    'FirmwareSerializer',
    'FirmwareAssignmentSerializer',
)

class FirmwareSerializer(NetBoxModelSerializer):
    manufacturer = ManufacturerSerializer(nested=True, required=True)
    device_type = DeviceTypeSerializer(many=True, nested=True, required=False)
    module_type = ModuleTypeSerializer(many=True, nested=True, required=False)
    class Meta:
        model = Firmware
        fields = '__all__'


class FirmwareAssignmentSerializer(NetBoxModelSerializer):
    firmware = FirmwareSerializer(nested=True, required=True)
    device = DeviceSerializer(nested=True, required=False)
    module = ModuleSerializer(nested=True, required=False)
    class Meta:
        model = FirmwareAssignment
        fields = '__all__'