# 🖼️ Views and Templates

The plugin uses NetBox UI helpers and standard `ViewSet` structures to display all data correctly. No custom HTML or JavaScript has been written — everything is based on existing NetBox components.

---

## 🧭 Navigation structure

After installation, two menu items appear:


* **Firmware**: shows a list of all firmware versions
* **Firmware Assignments**: list of all firmware assignments

Each item leads to a standard list view and detail page.

---

## 🔁 Overview of views

| View                         | Type       | Description                 |
| ---------------------------- | ---------- | --------------------------- |
| `FirmwareListView`           | ListView   | List with filters at the top|
| `FirmwareView`               | DetailView | Detail page with tables     |
| `FirmwareAssignmentListView` | ListView   | List of assignments         |
| `FirmwareAssignmentView`     | DetailView | Detail page per assignment  |

These views use NetBox’s `GenericUIViewSet` with automatically generated tables and breadcrumbs.

---

## 📂 Templates

The templates are generated based on the model structure and `NetBoxModelViewSet`. As a result, manual adjustment is usually unnecessary.

If you want to override a template, you can do so via:


```plaintext
<plugin_name>/templates/<app_label>/<model>_*.html
```


Example:

```plaintext
firmware/templates/firmware/firmware_list.html
```

But in this plugin, this has **not** been done.

---

## 🧩 Extra features


The plugin includes a small extension via `get_extra_actions()`:

* The "Assign firmware" button on a device detail page leads to a form that is pre-filled with that device.
* This is implemented via a custom URL and view that inherits from `CreateView` and performs contextual initialization.

Example:

```python
class AssignFirmwareToDeviceView(CreateView):
    def get_initial(self):
        return {'device': self.kwargs['device_pk']}
```

---

## 📚 Sources

* [NetBox plugins: Views](https://docs.netbox.dev/en/stable/plugins/views/)
* [Django Generic Views](https://docs.djangoproject.com/en/stable/ref/class-based-views/)

⬅️ [Back to overview](./index.md)
