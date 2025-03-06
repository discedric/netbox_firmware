from django import forms 
from .models import FirmwareForm

__all__ = (
)
"""
class FirmwareBulkAddForm(forms.Form):
    count = forms.IntegerField(
        min_value=1,
        required=True,
        help_text='How many Firmwares to create',
    )
    
class FirmwareBulkAddModelForm(FirmwareForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)"""