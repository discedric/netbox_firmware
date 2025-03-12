from django_tables2 import tables

from netbox.tables import NetBoxTable, columns
from .models import Firmware, FirmwareAssignment

from dcim.tables import DeviceTypeTable, ModuleTypeTable, RackTypeTable
from utilities.tables import register_table_column

__all__ = (
    'FirmwareTable',
    'FirmwareAssignmentTable',
)

class FirmwareTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )
    file_name = tables.Column()
    comments = tables.Column()
    status = tables.Column()
    manufacturer = tables.Column(
        verbose_name="Manufacturer",
        accessor='manufacturer',
        linkify=True,
        )
    device_type = tables.Column(
        accessor='device_type',
        linkify=True,
        )
    inventory_item_type = tables.Column(accessor='inventory_item_type')

    class Meta:
        model = Firmware
        fields = ('name', 'file_name', 'comments', 'status', 'manufacturer', 'device_type', 'inventory_item_type')
        attrs = {"class": "table table-striped table-bordered"}

class FirmwareAssignmentTable(NetBoxTable):
    description = tables.Column()
    ticket_number = tables.Column()
    patch_date = tables.Column()
    firmware = tables.Column(accessor='firmware.name',verbose_name='Firmware')
    manufacturer = tables.Column(accessor='manufacturer.name', verbose_name="Manufacturer")
    device_type = tables.Column(accessor='device_type.name')
    device = tables.Column(accessor='device.name')
    inventory_item = tables.Column(accessor='inventory_item.name', verbose_name='Inventory Item')
    inventory_item_type = tables.Column(accessor='inventory_item_type.name')

    class Meta:
        model = FirmwareAssignment
        fields = ('description','ticket_number','patch_date','firmware','manufacturer','device_type','device','inventory_item','inventory_item_type')
        attrs = {"class": "table table-striped table-bordered"}