from netbox.api.serializers import NetBoxModelSerializer
from dcim.api.serializers import DeviceTypeSerializer, ModuleTypeSerializer, DeviceSerializer, ModuleSerializer
from netbox_firmware.models import Bios, BiosAssignment


class BiosSerializer(NetBoxModelSerializer):
    device_type = DeviceTypeSerializer(nested=True, required=False)
    module_type = ModuleTypeSerializer(nested=True, required=False)
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