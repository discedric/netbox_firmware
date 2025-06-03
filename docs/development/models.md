# 📦 Models: Firmware and FirmwareAssignment

This plugin contains two core models that form the structure of the data storage:

---

## 📄 Firmware

The `Firmware` model defines a unique firmware version that you can assign to a device or module.

### 🔑 Key fields

| Field          | Type                   | Explanation                                     |
| -------------- | ---------------------- | ----------------------------------------------- |
| `name`         | CharField              | Name of the firmware version                    |
| `description`  | TextField              | Description of what the firmware is for         |
| `manufacturer` | ForeignKey             | The manufacturer of the firmware                |
| `device_type`  | ForeignKey (optional)  | Restricts the firmware to a specific device type|
| `module_type`  | ForeignKey (optional)  | Restricts the firmware to a specific module type|
| `file`         | FileField (optional)   | Uploadable attachment such as .bin or .pdf      |
| `status`       | CharField              | Choice of e.g. Draft, Active, Deprecated        |

### 🧠 Validation and filtering

* `device_type` and `module_type` are optional, but help with filtering.
* Firmware only appears for relevant types during an assignment.

### 📎 Code example

```python
class Firmware(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='firmware/', blank=True, null=True)
    manufacturer = models.ForeignKey(
        to='dcim.Manufacturer',
        on_delete=models.PROTECT,
    )
    device_type = models.ForeignKey(...)
    module_type = models.ForeignKey(...)
    status = models.CharField(...)
```

---

## 🔗 FirmwareAssignment

The `FirmwareAssignment` model links a `Firmware` to a `Device` or `Module`.

### 🔑 Fields

| Field           | Type                   | Explanation                           |
| --------------- | ---------------------- | ------------------------------------- |
| `firmware`      | ForeignKey             | Refers to a Firmware                  |
| `device`        | ForeignKey (optional)  | Where the firmware is applied         |
| `module`        | ForeignKey (optional)  | Alternative for device                |
| `patch_date`    | DateField              | Date when the firmware was applied    |
| `ticket_number` | CharField              | Internal reference                    |
| `comment`       | TextField              | Extra explanation                     |

### ⚖️ Validation

The `clean()` method ensures that you cannot fill in both a module and a device at the same time.

```python
def clean(self):
    if self.device and self.module:
        raise ValidationError("You may only fill in one of device/module.")
    if not self.device and not self.module:
        raise ValidationError("You must fill in at least device or module.")
```

---

## 📚 More info

* [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
* [NetBox Plugin Models](https://docs.netbox.dev/en/stable/plugins/models/)

⬅️ [Back to overview](./index.md)
