from django_tables2 import tables

from netbox.tables import NetBoxTable
from .models import Firmware

from dcim.tables import DeviceTypeTable, ModuleTypeTable, RackTypeTable
from utilities.tables import register_table_column

__all__ = (
    'FirmwareTable',
)

class FirmwareTable(NetBoxTable):
    name = tables.Column()
    description = tables.Column()
    status = tables.Column()
    manufacturer = tables.Column(accessor='manufacturer.name', verbose_name="Manufacturer")
    device_type = tables.Column(accessor='device_type.name')
    inventory_item_type = tables.Column(accessor='inventory_item_type.name')

    class Meta:
        model = Firmware
        fields = ('name', 'description', 'status', 'manufacturer', 'device_type', 'inventory_item_type')
        attrs = {"class": "table table-striped table-bordered"}