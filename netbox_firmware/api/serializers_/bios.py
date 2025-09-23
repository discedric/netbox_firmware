from netbox.api.serializers import NetBoxModelSerializer
from dcim.api.serializers import ManufacturerSerializer, DeviceTypeSerializer, ModuleTypeSerializer, DeviceSerializer, ModuleSerializer
from netbox_firmware.models import Bios, BiosAssignment

__all__ = (
    'BiosSerializer',
    'BiosAssignmentSerializer',
)

class BiosSerializer(NetBoxModelSerializer):
    manufacturer = ManufacturerSerializer(nested=True, required=True)
    device_type = DeviceTypeSerializer(many=True, nested=True, required=False)
    module_type = ModuleTypeSerializer(many=True, nested=True, required=False)
    class Meta:
        model = Bios
        fields = '__all__'


class BiosAssignmentSerializer(NetBoxModelSerializer):
    bios = BiosSerializer(nested=True, required=True)
    device = DeviceSerializer(nested=True, required=False)
    module = ModuleSerializer(nested=True, required=False)
    class Meta:
        model = BiosAssignment
        fields = '__all__'