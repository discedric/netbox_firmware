from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from ..choices import HardwareKindChoices, FirmwareStatusChoices
from netbox.models import NetBoxModel, ChangeLoggedModel, NestedGroupModel
from dcim.models import Manufacturer, DeviceType, ModuleType, Device, Module

class Firmware(NetBoxModel):
    #
    # fields that identify firmware
    #
    name = models.CharField(
        help_text='Name of the firmware',
        max_length=255,
        verbose_name='Name',
    )
    file_name = models.CharField(
        help_text='File name of the firmware',
        blank=True,
        null=True,
        max_length=255,
        verbose_name='File Name',
    )
    file = models.FileField(
        upload_to='firmware-files',
        help_text='File of the firmware',
        blank=True,
        null=True,
        verbose_name='File',
    )
    status = models.CharField(
        max_length=50,
        choices= FirmwareStatusChoices,
        default= FirmwareStatusChoices.STATUS_ACTIVE,
        help_text='Firmware lifecycle status',
    )
    description = models.CharField(
        help_text='Description of the firmware',
        max_length=255,
        verbose_name='Description',
        null=True,
        blank=True
    )
    comments = models.TextField(
        blank=True,
        null=True,
        help_text='Additional comments about the firmware',
    )
    
    #
    # hardware type fields
    #

    device_type = models.ManyToManyField(
        to=DeviceType,
        related_name='firmware',
        blank=True,
        verbose_name='Device Type',
    )
    module_type = models.ManyToManyField(
        to=ModuleType,
        related_name='firmware',
        blank=True,
        verbose_name='Module Type',
    )
    
    clone_fields = [
        'name','description', 'file_name', 'status', 'device_type',
        'comments', 'module_type'
    ]

    @property
    def kind(self):
        if self.device_type_id:
            return HardwareKindChoices.DEVICE
        elif self.module_type_id:
            return HardwareKindChoices.MODULE
        else:
            return None
        
    def get_kind_display(self):
        return dict(HardwareKindChoices)[self.kind]
    
    @property
    def filename(self):
        return self.file.name if self.file else None

    @property
    def hardware_type(self):
        return self.device_type or self.module_type or None
    
    @property
    def manufacturer(self):
        return self.get_manufacturer()
    
    def clean(self):
        return super().clean()

    def get_absolute_url(self):
        return reverse('plugins:netbox_firmware:firmware', args=[self.pk])
    
    @classmethod
    def get_fields(cls):
        return {field.name: field for field in cls._meta.get_fields()}
    
    def delete(self,*args, **kwargs):
        _name = self.file.name
        super().delete(*args, **kwargs)
        self.file.delete(save=False)
        self.file.name = _name

    class Meta:
        ordering = ('name',) # -> Fix ordering later
        verbose_name = 'Firmware'
        verbose_name_plural = 'Firmwares'
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message=_("The Firmware 'Name' must be unique.")
            ),
        ]

    def get_manufacturer(self):
        """Return manufacturer(s) based on device_type or module_type"""
        if self.device_type.exists():
            # return the manufacturer of the first related device_type
            return self.device_type.first().manufacturer

        if self.module_type.exists():
            # return the manufacturer of the first related module_type
            return self.module_type.first().manufacturer

        print("No manufacturer found")
        return None

    def __str__(self):
        return f'{self.name}'


class FirmwareAssignment(NetBoxModel):
    description = models.TextField(blank=True, null=True)
    ticket_number = models.CharField(max_length=100, blank=True, null=True)
    patch_date = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    firmware = models.ForeignKey(
        to=Firmware,
        related_name='FirmwareAssignment',
        on_delete=models.PROTECT,
        verbose_name='Firmware',
        null=True,
        blank=True
    )
    module = models.ForeignKey(
        to=Module,
        related_name='FirmwareAssignment',
        on_delete=models.PROTECT,
        verbose_name='Module',
        null=True,
        blank=True
    )
    device = models.ForeignKey(
        to=Device, 
        related_name='FirmwareAssignment',
        on_delete=models.PROTECT,
        verbose_name='Device',
        null=True, 
        blank=True
    )

    clone_fields = [
        'firmware', 'patch_date', 'description', 'comment', 'module', 'device'
    ]

    class Meta:
        ordering = ('firmware', 'device', 'module')
        verbose_name = 'Firmware Assignment'
        verbose_name_plural = 'Firmware Assignments'
        constraints = [
            models.CheckConstraint(
                check=models.Q(device__isnull=False) | models.Q(module__isnull=False),
                name='firmassign_either_device_or_module_required'
            ),
            models.UniqueConstraint(fields=['device'], name='unique_firmware_per_device'),
            models.UniqueConstraint(fields=['module'], name='unique_firmware_per_module'),
        ]

    @property
    def kind(self):
        if self.device_id:
            return HardwareKindChoices.DEVICE
        elif self.module_id:
            return HardwareKindChoices.MODULE
        else:
            return None
        
    def get_kind_display(self):
        return dict(HardwareKindChoices)[self.kind]

    @property
    def hardware(self):
        return self.device or self.module or None

    @property
    def hardware_type(self):
        return self.device_type or self.module_type or None

    @property
    def hardware_sn(self):
        return self.device.serial if self.device else self.module.serial if self.module else None

    @property
    def device_sn(self):
        return self.device.serial if self.device else None
    
    @property
    def module_device(self):
        return self.module.device if self.module else None
    
    @property
    def module_sn(self):
        return self.module.serial if self.module else None

    @property
    def device_type(self):
        return self.device.device_type if self.device else None
    
    @property
    def module_type(self):
        return self.module.module_type if self.module else None

    @property
    def manufacturer(self):
        return self.get_manufacturer()

    def get_manufacturer(self):
        """ Haalt de manufacturer op afhankelijk van device_type of module_type """
        if self.device:
            return self.device.device_type.manufacturer  # Haal de fabrikant via device_type
        elif self.module:
            return self.module.module_type.manufacturer  # Haal de fabrikant via module_type
        print('No manufacturer found')
        return None

    def __str__(self):
        if self.hardware:
            return f"{self.firmware} - {self.hardware}"
        return f"{self.firmware}"