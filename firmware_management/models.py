from django.db import models
from django.forms import ValidationError
from django.urls import reverse

from netbox.models import NetBoxModel, NestedGroupModel
from netbox_inventory.models import InventoryItemType

class Firmware(NetBoxModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deprecated', 'Deprecated'),
        ('beta', 'Beta'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True, 
        null=True
    )
    file_name = models.CharField(
        max_length=255
    )
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='active'
    )
    comment = models.TextField(
        blank=True, 
        null=True
    )
    manufacturer = models.ForeignKey(
        to='dcim.Manufacturer',
        on_delete=models.PROTECT,
        related_name='Firmware',
        blank=True,
        null=True,
        verbose_name='Manufacturer',
    )
    device_type = models.ForeignKey(
        to='dcim.DeviceType',
        on_delete=models.PROTECT,
        related_name='Firmware',
        blank=True,
        null=True,
        verbose_name='Device Type',
    )
    inventory_item_type = models.ForeignKey(
        InventoryItemType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f'{self.name} ({self.manufacturer.name})'


class FirmwareAssignment(NetBoxModel):
    inventory_item = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ticket_number = models.CharField(max_length=100, blank=True, null=True)
    patch_date = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    manufacturer = models.ForeignKey(
        to='dcim.Manufacturer', 
        related_name='FirmwareAssignment',
        on_delete=models.PROTECT,
        verbose_name='Manufacturer',
        null=True, 
        blank=True
    )
    device_type = models.ForeignKey(
        to='dcim.DeviceType',
        related_name='FirmwareAssignment',
        on_delete=models.PROTECT,
        verbose_name='Device Type',
        null=True, 
        blank=True
    )
    device = models.ForeignKey(
        to='dcim.Device', 
        related_name='FirmwareAssignment',
        on_delete=models.PROTECT,
        verbose_name='Device',
        null=True, 
        blank=True
    )
    inventory_item_type = models.ForeignKey(
        InventoryItemType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.device} - {self.device_type} - {self.inventory_item_type}"