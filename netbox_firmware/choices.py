from utilities.choices import ChoiceSet
from django.utils.translation import gettext_lazy as _


#
# Firmware
#

class FirmwareStatusChoices(ChoiceSet):
    key = 'Firmware.status'

    STATUS_ACTIVE = 'active'
    STATUS_STAGED = 'staged'
    STATUS_PLANNED = 'planned'
    STATUS_DECOMMISSIONING = 'decommissioning'
    STATUS_CORRUPTED = 'corrupted'
    STATUS_ARCHIVED = 'archived'
    

    CHOICES = [
        (STATUS_ACTIVE, _('Active'), 'green'),
        (STATUS_STAGED, _('Staged'), 'blue'),
        (STATUS_PLANNED, _('Planned'), 'cyan'),
        (STATUS_DECOMMISSIONING, _('Decommissioning'), 'yellow'),
        (STATUS_CORRUPTED, _('Corrupted'), 'red'),
        (STATUS_ARCHIVED, _('Archived'), 'purple'),
        
    ]

#
# Bios
#

class BiosStatusChoices(ChoiceSet):
    key = 'Bios.status'

    STATUS_ACTIVE = 'active'
    STATUS_STAGED = 'staged'
    STATUS_PLANNED = 'planned'
    STATUS_DECOMMISSIONING = 'decommissioning'
    STATUS_CORRUPTED = 'corrupted'
    STATUS_ARCHIVED = 'archived'
    

    CHOICES = [
        (STATUS_ACTIVE, _('Active'), 'green'),
        (STATUS_STAGED, _('Staged'), 'blue'),
        (STATUS_PLANNED, _('Planned'), 'cyan'),
        (STATUS_DECOMMISSIONING, _('Decommissioning'), 'yellow'),
        (STATUS_CORRUPTED, _('Corrupted'), 'red'),
        (STATUS_ARCHIVED, _('Archived'), 'purple'),
        
    ]

#
# General
#


class HardwareKindChoices(ChoiceSet):
    DEVICE = 'device'
    MODULE = 'module'

    CHOICES = [
        (DEVICE, 'Device'),
        (MODULE, 'Module'),
    ]