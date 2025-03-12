import django_filters
from netbox.filtersets import NetBoxModelFilterSet
from .models import Firmware, FirmwareAssignment

class FirmwareFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Firmware
        fields = {
            'name': ['exact', 'icontains'],
            'file_name': ['exact', 'icontains'],
            'status': ['exact'],
            'manufacturer': ['exact'],
            'device_type': ['exact'],
            'inventory_item_type': ['exact'],
        }

class FirmwareAssignmentFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = FirmwareAssignment
        fields = {
            'description': ['exact', 'icontains'],
            'ticket_number': ['exact', 'icontains'],
            'patch_date': ['exact'],
            'comment': ['exact', 'icontains'],
            'firmware': ['exact'],
            'manufacturer': ['exact'],
            'device_type': ['exact'],
            'device': ['exact'],
            'inventory_item': ['exact'],
            'inventory_item_type': ['exact'],
        }