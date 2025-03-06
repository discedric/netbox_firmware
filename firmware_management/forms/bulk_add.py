from django import forms 
from .models import FirmwareAssignmentForm

__all__ = (
    'FirmwareAssignmentBulkAddForm',
    'FirmwareAssignmentBulkAddModelForm',
)

class FirmwareAssignmentBulkAddForm(forms.Form):
    count = forms.IntegerField(
        min_value=1,
        required=True,
        help_text='How many Firmwares to create',
    )
    
class FirmwareAssignmentBulkAddModelForm(FirmwareAssignmentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)