from django.template import Template
from netbox.plugins import PluginTemplateExtension

from .models import Firmware, FirmwareAssignment, Bios, BiosAssignment
from .utils import query_located

### Firmware ###

### This will show all related Firmware for the manufacturer in the manufacturer view.
class FirmwareCountsManufacturer(PluginTemplateExtension):
    models = ['dcim.manufacturer']
    def right_page(self):
        object = self.context.get('object')
        user = self.context['request'].user
        count_device = Firmware.objects.restrict(user, 'view').filter(device_type__manufacturer=object).distinct().count()
        count_module = Firmware.objects.restrict(user, 'view').filter(module_type__manufacturer=object).distinct().count()
        context = {
            'firmware_stats': [
                {
                    'label': 'Devices',
                    'filter_field': 'manufacturer_id',
                    'extra_filter': '&kind=device',
                    'count': count_device,
                },
                {
                    'label': 'Modules',
                    'filter_field': 'manufacturer_id',
                    'extra_filter': '&kind=module',
                    'count': count_module,
                },
                {
                    'label': 'Total',
                    'filter_field': 'manufacturer_id',
                    'count': count_device + count_module,
                },
            ],
        }
        return self.render('netbox_firmware/inc/firmware_stats_counts.html', extra_context=context)

    

### This shows how many devices or modules that have this Firmware assigned in the Firmware view.
class FirmwareAssignmentsList(PluginTemplateExtension):
    models = ['netbox_firmware.firmware']
    kind = 'firmware'
  
    def right_page(self):
        object = self.context.get('object')
        assignments = FirmwareAssignment.objects.filter(**{f'{self.kind}':object.id})
        context = {
          #'assignments': assignments.order_by('-id')[:5], # Uncomment if you want a limited number of assignments visible in the model view
          'count': assignments.count()
        }
        return self.render('netbox_firmware/inc/firmware_assignment_list.html', extra_context=context)



### This is the base class for showing assigned firmware in the device or module view.
### The actual classes are below.
class FirmwareAssignedInfoExtension(PluginTemplateExtension):
    def right_page(self):
        object = self.context.get('object')
        assignments = FirmwareAssignment.objects.filter(**{f'{self.kind}_id':object.id}).order_by('-patch_date')[:5]
        context = {
          'assignments': assignments
        }
        return self.render('netbox_firmware/inc/firmware_info.html', extra_context=context)

### This will show assigned firmware for the device in the device view.
class FirmwareAssignmentInfoDevice(FirmwareAssignedInfoExtension):
    models = ['dcim.device']
    kind = 'device'

### This will show assigned firmware for the module in the module view.
class FirmwareAssignmentInfoModule(FirmwareAssignedInfoExtension):
    models = ['dcim.module']
    kind = 'module'



### This will show all compatible firmwares for the device type in the device type view.
class FirmwareListDeviceType(PluginTemplateExtension):
    models = ['dcim.devicetype']

    def right_page(self):
        firmwares = self.context['object'].firmware.all()
        return self.render("netbox_firmware/inc/firmware_devicetype_list.html", extra_context={"firmwares": firmwares})



### This will show all compatible firmwares for the module type in the module type view.
class FirmwareListModuleType(PluginTemplateExtension):
    models = ['dcim.moduletype']

    def right_page(self):
        firmwares = self.context['object'].firmware.all()
        return self.render("netbox_firmware/inc/firmware_moduletype_list.html", extra_context={"firmwares": firmwares})



## ---------------------------------------- ##



### BIOS ###


### This will show all related BIOS for the manufacturer in the manufacturer view.
class BiosCountsManufacturer(PluginTemplateExtension):
    models = ['dcim.manufacturer']
    def right_page(self):
        object = self.context.get('object')
        user = self.context['request'].user
        count_device = Bios.objects.restrict(user, 'view').filter(device_type__manufacturer=object).count()
        count_module = Bios.objects.restrict(user, 'view').filter(module_type__manufacturer=object).count()
        context = {
            'bios_stats': [
                {
                    'label': 'Devices',
                    'filter_field': 'manufacturer_id',
                    'extra_filter': '&kind=device',
                    'count': count_device,
                },
                {
                    'label': 'Modules',
                    'filter_field': 'manufacturer_id',
                    'extra_filter': '&kind=module',
                    'count': count_module,
                },
                {
                    'label': 'Total',
                    'filter_field': 'manufacturer_id',
                    'count': count_device + count_module,
                },
            ],
        }
        return self.render('netbox_firmware/inc/bios_stats_counts.html', extra_context=context)



### This shows how many devices or modules that have this BIOS assigned in the BIOS view.
class BiosAssignmentsList(PluginTemplateExtension):
    models = ['netbox_firmware.bios']
    kind = 'bios'
  
    def right_page(self):
        object = self.context.get('object')
        assignments = BiosAssignment.objects.filter(**{f'{self.kind}':object.id})
        context = {
          #'assignments': assignments.order_by('-id')[:5], # Uncomment if you want a limited number of assignments visible in the model view
          'count': assignments.count()
        }
        return self.render('netbox_firmware/inc/bios_assignment_list.html', extra_context=context)



### This is the base class for showing assigned BIOS in the device or module view.
### The actual classes are below.
class BiosAssignedInfoExtension(PluginTemplateExtension):
    def right_page(self):
        object = self.context.get('object')
        assignments = BiosAssignment.objects.filter(**{f'{self.kind}_id':object.id}).order_by('-patch_date')[:5]
        context = {
          'assignments': assignments
        }
        return self.render('netbox_firmware/inc/bios_info.html', extra_context=context)

### This will show assigned BIOS for the device in the device view.
class BiosAssignmentInfoDevice(BiosAssignedInfoExtension):
    models = ['dcim.device']
    kind = 'device'

### This will show assigned BIOS for the module in the module view.
class BiosAssignmentInfoModule(BiosAssignedInfoExtension):
    models = ['dcim.module']
    kind = 'module'



### This will show all compatible BIOS for the device type in the device type view.
class BiosListDeviceType(PluginTemplateExtension):
    models = ['dcim.devicetype']

    def right_page(self):
        bios = self.context['object'].bios.all()
        return self.render("netbox_firmware/inc/bios_devicetype_list.html", extra_context={"bios": bios})



### This will show all compatible firmwares for the module type in the module type view.
class BiosListModuleType(PluginTemplateExtension):
    models = ['dcim.moduletype']

    def right_page(self):
        bios = self.context['object'].bios.all()
        return self.render("netbox_firmware/inc/bios_moduletype_list.html", extra_context={"bios": bios})


## ---------------------------------------- ##


template_extensions = (
    FirmwareCountsManufacturer,
    FirmwareListDeviceType,
    FirmwareListModuleType,
    FirmwareAssignmentsList,
    FirmwareAssignmentInfoDevice,
    FirmwareAssignmentInfoModule,
    BiosCountsManufacturer,
    BiosListDeviceType,
    BiosListModuleType,
    BiosAssignmentsList,
    BiosAssignmentInfoDevice,
    BiosAssignmentInfoModule,
)