from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from ..choices import HardwareKindChoices, FirmwareStatusChoices
from netbox.models import NetBoxModel, ChangeLoggedModel, NestedGroupModel
from dcim.models import Manufacturer, DeviceType, ModuleType, Device, Module


### ------------------------------------------------------- ###
### Firmware Model
### ------------------------------------------------------- ###


class Firmware(NetBoxModel):
    #
    ### Fields that identify firmware ###
    #
    name = models.CharField(
        help_text='Name of the firmware',
        max_length=255,
        verbose_name='Name',
    )
    manufacturer = models.ForeignKey(
        help_text='Name of the manufacturer',
        to= 'dcim.Manufacturer',
        on_delete=models.PROTECT,
        related_name="Firmware",
        # default=22,  # Uncomment and set to a valid Manufacturer ID for existing records without a manufacturer.
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
    ### Hardware Type fields ###
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
        'name', 'manufacturer', 'description', 'status', 'device_type', 'module_type'
    ]


    class Meta:
        ordering = ('name',)
        verbose_name = 'Firmware'
        verbose_name_plural = 'Firmwares'
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message=_("The Firmware 'Name' must be unique.")
            ),
        ]

    ### Get all fields of the model ?
    @classmethod
    def get_fields(cls):
        return {field.name: field for field in cls._meta.get_fields()}

    #
    ### Properties ###
    #

    ### This property is needed to check if the firmware is for Devices or Modules and also to filter the template and show only the assigned Device Types / Hide Module Types.
    ### We need to use .exists() because it's a ManyToMany field.
    @property
    def kind(self):
        if self.device_type.exists():
            return HardwareKindChoices.DEVICE
        elif self.module_type.exists():
            return HardwareKindChoices.MODULE
        return None

    ### Needed to show File Path in the Firmware Table
    @property
    def file_path(self):
        return self.file.name if self.file else None

    @property
    def hardware_type(self):
        return self.device_type or self.module_type or None

    ### This property is needed to filter the template and show only the assigned Device Types / Hide Module Types
    @property
    def has_device_type(self):
        return self.device_type.exists()

    ### This property is needed to filter the template and show only the assigned Module Types / Hide Device Types
    @property
    def has_module_type(self):
        return self.module_type.exists()


    #
    ### Main definitions ###
    #

    ### This is needed for bulk import/export and other places where the kind of hardware is needed.    
    def get_kind_display(self):
        return dict(HardwareKindChoices)[self.kind]

    ### This will disable changing the Manufacturer once a Device Type or Module Type is assigned
    def clean(self):
        if self.pk:
            old = Firmware.objects.get(pk=self.pk)

            # Check if manufacturer changed
            if old.manufacturer != self.manufacturer:
                # Only lock if already linked to device_type(s) or module_type(s)
                if self.device_type.exists() or self.module_type.exists():
                    raise ValidationError({
                        "manufacturer": (
                            "The manufacturer cannot be changed because this firmware "
                            "is already linked to one or more device types or module types."
                        )
                    })

        return super().clean()

    ### This will return the URL to the firmware detail view.
    def get_absolute_url(self):
        return reverse('plugins:netbox_firmware:firmware', args=[self.pk])
    
    ### This will delete the file from the storage when the Firmware object is deleted.
    def delete(self,*args, **kwargs):
        _name = self.file.name
        super().delete(*args, **kwargs)
        self.file.delete(save=False)
        self.file.name = _name

    ### This is how the firmware will be displayed in the lists using his name.
    def __str__(self):
        return f'{self.name}'



### ------------------------------------------------------ ###
### Firmware Assignment Model
### ------------------------------------------------------ ###


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

    #
    ### Properties ###
    #

    @property
    def kind(self):
        if self.device_id:
            return HardwareKindChoices.DEVICE
        elif self.module_id:
            return HardwareKindChoices.MODULE
        else:
            return None
        
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

    #
    ### Main definitions ###
    #

    def get_kind_display(self):
        return dict(HardwareKindChoices)[self.kind]

    ### Needed to get the manufacturer depending on device_type or module_type
    def get_manufacturer(self):
        """ Get manufacturer depending on device_type or module_type """
        if self.device:
            return self.device.device_type.manufacturer
        elif self.module:
            return self.module.module_type.manufacturer
        print('No manufacturer found')
        return None

    def __str__(self):
        if self.hardware:
            return f"{self.firmware} - {self.hardware}"
        return f"{self.firmware}"