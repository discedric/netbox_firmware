# Forms and Validation in the NetBox Firmware Plugin

## Why forms?

Forms are used to validate and structure user input, for example when adding or editing firmware or assignments.

## Location

The forms are in `forms.py`.

## Main functionalities

- Validation via `clean()` methods
- Dynamic choice fields depending on device_type/module_type
- Custom widgets for better UX

## Example validation in `FirmwareAssignmentForm`:

```python
def clean(self):
    cleaned_data = super().clean()
    device = cleaned_data.get("device")
    module = cleaned_data.get("module")
    if device and module:
        raise ValidationError("You may only fill in one of device or module.")
    if not device and not module:
        raise ValidationError("You must fill in either a device or a module.")
    return cleaned_data