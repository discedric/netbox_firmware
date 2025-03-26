from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify

from dcim.models import DeviceType, Location, Manufacturer, ModuleType, RackType, Site
from netbox.forms import NetBoxModelBulkEditForm, NetBoxModelImportForm
from dcim.choices import DeviceStatusChoices
from tenancy.models import Contact, ContactGroup, Tenant
from utilities.forms import add_blank_choice
from utilities.forms.fields import (
    CommentField,
    CSVChoiceField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
)
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import DatePicker

from ..choices import FirmwareStatusChoices
from ..models import (
    Firmware,
    FirmwareAssignment
)
from ..utils import get_plugin_setting

class FirmwareBulkEditForm(NetBoxModelBulkEditForm):
    name = forms.CharField(required=False,)
    description = forms.CharField(max_length=200, required=False)
    status = forms.ChoiceField(
        choices=add_blank_choice(DeviceStatusChoices),
        required=False,
        initial='',
    )
    file_name= forms.CharField(required=False,)
    