# Tables Documentation

The `tables` module provides table definitions for displaying firmware and BIOS data in tabular format within the NetBox UI. These tables are used to present data in a user-friendly and sortable manner.

## Key Tables

### FirmwareTable
- **Purpose**: Displays a list of firmware objects.
- **Columns**:
  - `name`: Name of the firmware.
  - `status`: Lifecycle status.
  - `manufacturer`: Associated manufacturer.
  - `hardware_type`: The hardware type the firmware is linked to.

### FirmwareAssignmentTable
- **Purpose**: Displays a list of firmware assignments.
- **Columns**:
  - `firmware`: The firmware being assigned.
  - `device`, `module`, `inventory_item`: The hardware receiving the firmware.
  - `patch_date`: Date of the firmware patch.

## Features
- Supports sorting and filtering.
- Integrates with NetBox's bulk actions for editing and deleting records.

## Usage
These tables are used in list views to provide an overview of firmware and assignments. They are defined using the `django-tables2` library.