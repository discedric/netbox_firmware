from netbox.search import SearchIndex, register_search
from . import models

@register_search
class FirmwareIndex(SearchIndex):
    model = models.Firmware
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs =(
        'status', 'manufacturer'
    )
    
@register_search
class FirmwareAssignmentIndex(SearchIndex):
    model = models.FirmwareAssignment
    fields = (
        ('firmware', 100),
        ('device', 100),
        ('module', 100),
        ('description',500),
        ('comment', 5000),
    )
    display_attrs = (
        'firmware', 'device', 'module'
    )

@register_search
class BiosIndex(SearchIndex):
    model = models.Bios
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs = (
        'status', 'manufacturer'
    )

@register_search
class BiosAssignmentIndex(SearchIndex):
    model = models.BiosAssignment
    fields = (
        ('bios', 100),
        ('device', 100),
        ('module', 100),
        ('description', 500),
        ('comment', 5000),
    )
    display_attrs = (
        'bios', 'device', 'module'
    )