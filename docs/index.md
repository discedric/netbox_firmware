
# 📁 NetBox Firmware Plugin – Documentation

This folder contains all explanations about the operation of the [`netbox_firmware`](https://github.com/discedric/netbox_firmware) plugin. This document is intended for people with little or no experience with NetBox, Django, or plugin development.

---


## 📌 Contents

- [📁 NetBox Firmware Plugin – Documentation](#-netbox-firmware-plugin--documentation)
  - [📌 Contents](#-contents)
  - [What does this plugin do?](#what-does-this-plugin-do)
  - [Models](#models)
    - [1. `Firmware`](#1-firmware)
    - [2. `FirmwareAssignment`](#2-firmwareassignment)
  - [Used technologies](#used-technologies)
  - [API functionality](#api-functionality)
  - [Installation](#installation)
  - [User guide](#user-guide)
    - [Add new firmware](#add-new-firmware)
    - [Create assignment](#create-assignment)
  - [Links and resources](#links-and-resources)

---


## What does this plugin do?

This plugin extends NetBox with the ability to manage **firmware versions** and their **installations on devices**. It allows you to record:

* which firmware versions exist,
* which devices or modules use that firmware,
* when an upgrade was performed,
* which ticket number is associated,
* optionally: a firmware file.

The goal is to provide an **overview and history of firmware updates** in your infrastructure.

---


## Models

### 1. `Firmware`

Information about a specific firmware version:

| Field                        | Explanation                                              |
| ---------------------------- | -------------------------------------------------------- |
| `name`                       | Name of the firmware                                     |
| `description`                | Description                                              |
| `manufacturer`               | Manufacturer                                             |
| `device_type` / `module_type`| (optional) For which device/module type is it intended   |
| `file_name`                  | Optional, extra name for the file                        |
| `file`                       | Optional, upload of e.g. `.bin` or `.pdf` file           |
| `status`                     | Active / deprecated / draft                              |


### 2. `FirmwareAssignment`

Link between a firmware and a device/module:

| Field               | Explanation                    |
| ------------------- | ------------------------------ |
| `firmware`          | Which firmware version         |
| `device` / `module` | Where it is applied            |
| `patch_date`        | When it was installed          |
| `ticket_number`     | Internal ticket code (optional)|
| `comment`           | Free comments                  |

It is automatically validated that either a device or a module is filled in (but never both).

---


## Used technologies

This plugin uses:

* 🧰 **[NetBox](https://netbox.dev/)** – the main platform
* 🧱 **[Django](https://www.djangoproject.com/)** – for data models and admin UI
* ⚙️ **[Django REST Framework](https://www.django-rest-framework.org/)** – for API endpoints
* 📦 **[Python 3.12+]** – programming language

---


## API functionality

The plugin automatically provides endpoints via NetBox:

* `/api/plugins/firmware/firmwares/`
* `/api/plugins/firmware/assignments/`

These are compatible with the browsable API of DRF and NetBox’s own API documentation.

---


## Installation

1. Clone this repo into your NetBox plugins folder:

```bash
git clone https://github.com/discedric/netbox_firmware plugins/netbox_firmware
```

2. Enable the plugin in `configuration.py`:

```python
PLUGINS = [
  'netbox_firmware',
]
```

3. Install in your venv:

```bash
source /opt/netbox/venv/bin/activate
pip install -e /opt/netbox/netbox/netbox/plugins/netbox_firmware
```

4. Run migrations:

```bash
cd /opt/netbox/netbox
python3 manage.py migrate
```

5. Reload the index:

```bash
cd /opt/netbox/netbox
python3 manage.py reindex
```

---


## User guide

### Add new firmware

* Go to the menu `Plugins > Firmware > Firmwares`
* Click on `Add`
* Fill in name, manufacturer, file, and optionally device/module type

### Create assignment

* Go to `Firmware Assignments`
* Click on `Add`
* Choose a firmware, link to a module or device
* Fill in date and optionally a ticket number

---


## Links and resources

| Subject            | Link                                                                                                                        |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| NetBox             | [https://netbox.dev](https://netbox.dev)                                                                                    |
| Plugin documentation| [https://docs.netbox.dev/en/stable/plugins/development/](https://docs.netbox.dev/en/stable/plugins/development/)           |
| Django models      | [https://docs.djangoproject.com/en/stable/topics/db/models/](https://docs.djangoproject.com/en/stable/topics/db/models/)    |
| Django admin       | [https://docs.djangoproject.com/en/stable/ref/contrib/admin/](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)  |
| REST API           | [https://www.redhat.com/en/topics/api/what-is-a-rest-api](https://www.redhat.com/en/topics/api/what-is-a-rest-api)          |
| Plugin repo        | [https://github.com/discedric/netbox_firmware](https://github.com/discedric/netbox_firmware)                               |

---