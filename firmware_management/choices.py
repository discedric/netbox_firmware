from utilities.choices import ChoiceSet


#
# Firmware
#

class FirmwareStatusChoices(ChoiceSet):
    key = 'Firmware.status'

    CHOICES = [
        ('active', 'Active'),
        ('deprecated', 'Deprecated'),
        ('beta', 'Beta'),
        ('archived', 'Archived'),
    ]


class HardwareKindChoices(ChoiceSet):
    CHOICES = [
        ('device', 'Device'),
        ('module', 'Module'),
        ('inventoryitem', 'Inventory Item'),
        ('rack', 'Rack'),
    ]