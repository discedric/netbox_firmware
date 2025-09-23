from django_tables2 import tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, columns
from ..models import Bios, BiosAssignment
from netbox_firmware.utils import BiosColumn

from dcim.tables import DeviceTable, ModuleTable
from utilities.tables import register_table_column

from .template_code import *

__all__ = (
    'BiosTable',
    'BiosAssignmentTable',
)

class BiosTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )
    description = tables.Column()
    file_name = tables.Column()
    comments = tables.Column()
    status = tables.Column()
    manufacturer = tables.Column(
        verbose_name=_('Manufacturer'),
        linkify=True,
    )
    device_type = columns.TemplateColumn(
        template_code=SHOW_LINKED_DEVICE_TYPES,
        linkify=True,
        )
    module_type = columns.TemplateColumn(
        template_code=SHOW_LINKED_MODULE_TYPES,
        linkify=True,
        )
    instance_count = columns.LinkedCountColumn(
        viewname='plugins:netbox_firmware:biosassignment_list',
        url_params={'bios_id': 'pk'},
        verbose_name=_('Instances')
    )
    file_path = tables.Column(
        accessor='file_path',
        verbose_name=_('File path'),
        orderable=False
    )

    class Meta(NetBoxTable.Meta):
        model = Bios
        fields = ('name', 'file_name', 'comments', 'status', 
                  'manufacturer', 
                  'module_type', 'device_type'
                  )
        #░ Default columns moeten nog gedefinieerd worden in de Meta class

    # def order_manufacturer(self, queryset, is_descending):
    #     if is_descending:
    #         ordering_device = '-device_type__manufacturer'
    #         ordering_module = '-module_type__manufacturer'
    #     else:
    #         ordering_device = 'device_type__manufacturer'
    #         ordering_module = 'module_type__manufacturer'
    
    #     # Voeg de twee velden toe aan de query voor een gecombineerde sortering
    #     queryset = queryset.order_by(ordering_device, ordering_module)
    #     return queryset, True

class BiosAssignmentTable(NetBoxTable):
    description = tables.Column()
    ticket_number = tables.Column()
    patch_date = tables.Column()
    bios = tables.Column(accessor='bios',verbose_name='BIOS',linkify=True,)
    module = tables.Column(accessor='module',verbose_name="Module",linkify=True,)
    module_device= tables.Column(accessor='module_device',verbose_name='Module owner',linkify=True)
    device = tables.Column(accessor='device',verbose_name="Device",linkify=True,)
    manufacturer = tables.Column(
        verbose_name=_('Manufacturer'),
        accessor='get_manufacturer',  # We gebruiken de method get_manufacturer
        linkify=True,
    )
    
    device_type = tables.Column(accessor='device_type',verbose_name='Device Type',linkify=True)
    device_sn = tables.Column(accessor='device_sn',verbose_name='Device Serial Number')
    module_type = tables.Column(accessor='module_type',verbose_name='Module Type',linkify=True)
    module_sn = tables.Column(accessor='module_sn',verbose_name='Module Serial Number')
    
    class Meta(NetBoxTable.Meta):
        model = BiosAssignment
        fields = ('description','ticket_number','patch_date',
                  'bios','device', 'module'
                  )

    # Order methods
    def order_manufacturer(self, queryset, is_descending):
        if is_descending:
            ordering_device = '-device__device_type__manufacturer'
            ordering_module = '-module__module_type__manufacturer'
        else:
            ordering_device = 'device__device_type__manufacturer'
            ordering_module = 'module__module_type__manufacturer'
    
        # Voeg de twee velden toe aan de query voor een gecombineerde sortering
        queryset = queryset.order_by(ordering_device, ordering_module)
        return queryset, True

    def order_device_sn(self, queryset, is_descending):
        ordering = ('-device__serial' if is_descending else 'device__serial')
        queryset = queryset.order_by(ordering)
        return queryset, True

    def order_module_device(self, queryset, is_descending):
        ordering = ('-module__device' if is_descending else 'module__device')
        queryset = queryset.order_by(ordering)
        return queryset, True
    
    def order_module_sn(self, queryset, is_descending):
        ordering = ('-module__serial' if is_descending else 'module__serial')
        queryset = queryset.order_by(ordering)
        return queryset, True

    def order_device_type(self, queryset, is_descending):
        ordering = ('-device__device_type__model' if is_descending else 'device__device_type__model')
        queryset = queryset.order_by(ordering)
        return queryset, True

    def order_module_type(self, queryset, is_descending):
        ordering = ('-module__module_type__model' if is_descending else 'module__module_type__model')
        queryset = queryset.order_by(ordering)
        return queryset, True

# ========================
# DCIM model table columns
# ========================


### Add BIOS column to Device and Module tables.
bios_column = BiosColumn(
    verbose_name=_('BIOS'),
    orderable=True,
)

register_table_column(bios_column, 'BiosAssignment', DeviceTable)
register_table_column(bios_column, 'BiosAssignment', ModuleTable)