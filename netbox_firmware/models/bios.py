from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from ..choices import HardwareKindChoices, BiosStatusChoices
from netbox.models import NetBoxModel, ChangeLoggedModel, NestedGroupModel
from dcim.models import Manufacturer, DeviceType, ModuleType, Device, Module


### ------------------------------------------------------- ###
### BIOS Model
### ------------------------------------------------------- ###


class Bios(NetBoxModel):
    #
    # fields that identify bios
    #
    name = models.CharField(
        help_text='Name of the bios',
        max_length=255,
        verbose_name='Name',
    )
    manufacturer = models.ForeignKey(
        help_text='Name of the manufacturer',
        to= 'dcim.Manufacturer',
        on_delete=models.PROTECT,
        related_name="bios",
        # default=22,  # Uncomment and set to a valid Manufacturer ID for existing records without a manufacturer.
    )
    file_name = models.CharField(
        help_text='File name of the bios',
        blank=True,
        null=True,
        max_length=255,
        verbose_name='File Name',
    )
    file = models.FileField(
        upload_to='bios-files',
        help_text='File of the bios',
        blank=True,
        null=True,
        verbose_name='File',
    )
    status = models.CharField(
        max_length=50,
        choices= BiosStatusChoices,
        default= BiosStatusChoices.STATUS_ACTIVE,
        help_text='Bios lifecycle status',
    )
    description = models.CharField(
        help_text='Description of the bios',
        max_length=255,
        verbose_name='Description',
        null=True,
        blank=True
    )
    comments = models.TextField(
        blank=True,
        null=True,
        help_text='Additional comments about the bios',
    )
    
    #
    ### Hardware Type fields ###
    #

    device_type = models.ManyToManyField(
        to=DeviceType,
        related_name='bios',
        blank=True,
        verbose_name='Device Type',
    )
    module_type = models.ManyToManyField(
        to=ModuleType,
        related_name='bios',
        blank=True,
        verbose_name='Module Type',
    )
    
    clone_fields = [
        'name', 'manufacturer', 'description', 'status', 'device_type', 'module_type'
    ]
    

    class Meta:
        ordering = ('name',)
        verbose_name = 'BIOS'
        verbose_name_plural = 'BIOS'
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message=_("The BIOS 'Name' must be unique.")
            ),
        ]
    
    ### Get all fields of the model ?
    @classmethod
    def get_fields(cls):
        return {field.name: field for field in cls._meta.get_fields()}

        #
    ### Properties ###
    #

    ### This property is needed to check if the BIOS is for Devices or Modules and also to filter the template and show only the assigned Device Types / Hide Module Types.
    ### We need to use .exists() because it's a ManyToMany field.
    @property
    def kind(self):
        if self.device_type_id:
            return HardwareKindChoices.DEVICE
        elif self.module_type_id:
            return HardwareKindChoices.MODULE
        else:
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
            old = Bios.objects.get(pk=self.pk)

            # Check if manufacturer changed
            if old.manufacturer != self.manufacturer:
                # Only lock if already linked to device_type(s) or module_type(s)
                if self.device_type.exists() or self.module_type.exists():
                    raise ValidationError({
                        "manufacturer": (
                            "The manufacturer cannot be changed because this bios "
                            "is already linked to one or more device types or module types."
                        )
                    })

        return super().clean()

    ### This will return the URL to the bios detail view.
    def get_absolute_url(self):
        return reverse('plugins:netbox_firmware:bios', args=[self.pk])

    ### This will delete the file from the storage when the BIOS object is deleted.
    def delete(self,*args, **kwargs):
        _name = self.file.name
        super().delete(*args, **kwargs)
        self.file.delete(save=False)
        self.file.name = _name

    ### This is how the firmware will be displayed in the lists using his name.
    def __str__(self):
        return f'{self.name}'



### ------------------------------------------------------ ###
### BIOS Assignment Model
### ------------------------------------------------------ ###


class BiosAssignment(NetBoxModel):
    description = models.TextField(blank=True, null=True)
    ticket_number = models.CharField(max_length=100, blank=True, null=True)
    patch_date = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    bios = models.ForeignKey(
        to=Bios,
        related_name='BiosAssignment',
        on_delete=models.PROTECT,
        verbose_name='BIOS',
        null=True,
        blank=True
    )
    module = models.ForeignKey(
        to=Module,
        related_name='BiosAssignment',
        on_delete=models.PROTECT,
        verbose_name='Module',
        null=True,
        blank=True
    )
    device = models.ForeignKey(
        to=Device, 
        related_name='BiosAssignment',
        on_delete=models.PROTECT,
        verbose_name='Device',
        null=True, 
        blank=True
    )

    clone_fields = [
        'bios', 'patch_date', 'description', 'comment', 'module', 'device'
    ]

    class Meta:
        ordering = ('bios', 'device', 'module')
        verbose_name = 'BIOS Assignment'
        verbose_name_plural = 'BIOS Assignments'
        constraints = [
            models.CheckConstraint(
                check=models.Q(device__isnull=False) | models.Q(module__isnull=False) ,
                name='bios_device_or_module_required'
            ),
            models.UniqueConstraint(fields=['device'], name='unique_bios_per_device'),
            models.UniqueConstraint(fields=['module'], name='unique_bios_per_module'),
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
    def module_device(self):
        return self.module.device if self.module else None
    
    @property
    def hardware_sn(self):
        return self.device.serial if self.device else self.module.serial if self.module else None

    @property
    def hardware_type(self):
        if self.device and self.device.device_type:
            return self.device.device_type
        if self.module and self.module.module_type:
            return self.module.module_type
        return None
    
    @property
    def hardware(self):
        return self.device or self.module or None
    
    @property
    def device_sn(self):
        return self.device.serial if self.device else None
    
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
            return f"{self.bios} - {self.hardware}"
        return f"{self.bios}"

