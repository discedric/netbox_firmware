# 📁 NetBox Firmware Plugin – Documentation

This folder contains all explanations about the operation of the [`netbox_firmware`](https://github.com/discedric/netbox_firmware) plugin. This document is intended for anyone who wants to use, understand, maintain, or extend the plugin. We explain step by step what the plugin does, how it is technically structured, and how you can make your own modifications.

---

## 📌 Contents

* [1. What does this plugin do?](#1-what-does-this-plugin-do)
* [2. Architecture and models](models.md)
* [3. API functionality](api.md)
* [4. Usage in the UI](ui.md)
* [5. Filters](filters.md)
* [6. Forms](forms.md)
* [7. URLs](urls.md)
* [8. Plugin structure and maintenance](structure.md)
* [9. Common errors and debugging](debugging.md)
* [10. Useful links and resources](resources.md)

---

## 1. What does this plugin do?

This plugin extends NetBox with the ability to manage **firmware versions** and assign them to **devices** or **modules**.

You can:

* Register firmware versions (name, description, manufacturer, file, status)
* Create assignments of firmware to devices/modules
* See when a firmware was applied and with which ticket number

Goal: to maintain an overview and history of firmware updates in an infrastructure.

More details can be found in [models.md](models.md).

---

Continue reading in the following documents:

* [models.md](models.md) – explanation of the data models and validation
* [api.md](api.md) – available API endpoints
* [ui.md](ui.md) – how the plugin looks and works in the NetBox interface
* [installation.md](installation.md) – how to install the plugin
* [structure.md](structure.md) – folders and files in the plugin
* [debugging.md](debugging.md) – tips for troubleshooting
* [resources.md](resources.md) – external links and official resources