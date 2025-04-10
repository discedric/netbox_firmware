from django_tables2 import tables

from netbox.tables import NetBoxTable, columns
from ..models import Bios, BiosAssignment

from dcim.tables import DeviceTypeTable, ModuleTypeTable, RackTypeTable
from utilities.tables import register_table_column

__all__ = (
    'BiosTable',
    'BiosAssignmentTable',
)

class BiosTable(NetBoxTable):
    """"
     zorg voor een counter zodat je ziet hoeveel keer deze assigned is
    """
    name = tables.Column(
        linkify=True,
    )
    file_name = tables.Column()
    comments = tables.Column()
    status = tables.Column()
    device_type = tables.Column(
        accessor='device_type',
        linkify=True,
        )
    module_type = tables.Column(
        accessor='module_type',
        linkify=True,
        )
    inventory_item_type = tables.Column(accessor='inventory_item_type', linkify=True)
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = Bios
        fields = ('name', 'file_name', 'comments', 'status', 
                  'module_type', 'device_type', 'inventory_item_type',
                  'actions'
                  )

class BiosAssignmentTable(NetBoxTable):
    description = tables.Column()
    ticket_number = tables.Column()
    patch_date = tables.Column()
    bios = tables.Column(accessor='bios',verbose_name='Bios',linkify=True,)
    module = tables.Column(accessor='module',verbose_name="Module",linkify=True,)
    device = tables.Column(accessor='device',verbose_name="Device",linkify=True,)
    inventory_item = tables.Column(accessor='inventory_item', verbose_name='Inventory Item',linkify=True,)
    actions = columns.ActionsColumn()
    
    class Meta(NetBoxTable.Meta):
        model = BiosAssignment
        fields = ('description','ticket_number','patch_date',
                  'firmware','device',
                  'inventory_item', 'module'
                  )

