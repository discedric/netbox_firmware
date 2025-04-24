from django_tables2 import tables
from django.utils.translation import gettext_lazy as _

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
    description = tables.Column()
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
    instance_count = columns.LinkedCountColumn(
        viewname='plugins:firmware_management:biosassignment_list',
        url_params={'bios_id': 'pk'},
        verbose_name=_('Instances')
    )
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = Bios
        fields = ('name', 'description', 'file_name', 'comments', 'status', 
                  'module_type', 'device_type',
                  'actions'
                  )
        

class BiosAssignmentTable(NetBoxTable):
    description = tables.Column()
    ticket_number = tables.Column()
    patch_date = tables.Column()
    bios = tables.Column(accessor='bios',verbose_name='BIOS',linkify=True,)
    module = tables.Column(accessor='module',verbose_name="Module",linkify=True,)
    module_device= tables.Column(accessor='module_device',verbose_name='Module owner',linkify=True)
    device = tables.Column(accessor='device',verbose_name="Device",linkify=True,)
    actions = columns.ActionsColumn()
    
    device_type = tables.Column(accessor='device_type',verbose_name='Device Type',linkify=True)
    device_sn = tables.Column(accessor='device_sn',verbose_name='Device Serial',linkify=True)
    module_type = tables.Column(accessor='module_type',verbose_name='Module Type',linkify=True)
    module_sn = tables.Column(accessor='module_sn',verbose_name='Module Serial',linkify=True)
    
    class Meta(NetBoxTable.Meta):
        model = BiosAssignment
        fields = ('description','ticket_number','patch_date',
                  'bios','device', 'module'
                  )

