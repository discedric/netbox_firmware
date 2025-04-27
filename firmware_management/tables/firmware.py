from django_tables2 import tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, columns
from ..models import Firmware, FirmwareAssignment

from dcim.tables import DeviceTypeTable, ModuleTypeTable, RackTypeTable
from utilities.tables import register_table_column

__all__ = (
    'FirmwareTable',
    'FirmwareAssignmentTable',
)

class FirmwareTable(NetBoxTable):
    """"
     zorg voor een counter zodat je ziet hoeveel keer deze assigned is
    """
    name = tables.Column(
        linkify=True,
    )
    file_name = tables.Column()
    description = tables.Column()
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
    module_type = tables.Column(
        accessor='module_type',
        linkify=True,
        )
    instance_count = columns.LinkedCountColumn(
        viewname='plugins:firmware_management:firmwareassignment_list',
        url_params={'firmware_id': 'pk'},
        verbose_name=_('Instances')
    )
    filename = tables.Column(
        accessor='filename',
        verbose_name=_('File path'),
    )
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = Firmware
        fields = ('name', 'file_name', 'comments', 'status', 
                  'manufacturer', 
                  'module_type', 'device_type',
                  'actions'
                  )
        

class FirmwareAssignmentTable(NetBoxTable):
    description = tables.Column()
    ticket_number = tables.Column()
    patch_date = tables.Column()
    firmware = tables.Column(accessor='firmware',verbose_name='Firmware',linkify=True,)
    manufacturer = tables.Column(accessor='manufacturer', verbose_name="Manufacturer",linkify=True,)
    device_type = tables.Column(accessor='device_type',verbose_name="Device Type",linkify=True,)
    module_type = tables.Column(accessor='module_type',linkify=True,)
    module = tables.Column(accessor='module',verbose_name="Module",linkify=True,)
    device = tables.Column(accessor='device',verbose_name="Device",linkify=True,)

    module_device= tables.Column(accessor='module_device',verbose_name='Module owner',linkify=True)
    device_sn = tables.Column(accessor='device_sn',verbose_name='Device Serial',linkify=True)
    module_sn = tables.Column(accessor='module_sn',verbose_name='Module Serial',linkify=True)
    
    class Meta(NetBoxTable.Meta):
        model = FirmwareAssignment
        fields = ('description','ticket_number','patch_date',
                  'firmware','manufacturer',
                  'device_type','device',
                  'module','module_type'
                  )
        default_columns=(
            'firmware', 'description', 'patch_date', 
            'device', 'module',
            'manufacturer', 'ticket_number',
        )
        

