# Models Documentation

The `models` module defines the database schema for firmware and BIOS objects. These models represent the core data structures used by the plugin.

## Key Models

### Firmware
- **Purpose**: Represents a firmware object.
- **Fields**:
  - `name`: Name of the firmware.
  - `file_name`: File name of the firmware.
  - `status`: Lifecycle status (e.g., Active, Deprecated).
  - `manufacturer`: Associated manufacturer.
  - `device_type`, `module_type`, `inventory_item_type`: Hardware types the firmware is associated with.

### FirmwareAssignment
- **Purpose**: Represents the assignment of firmware to a device, module, or inventory item.
- **Fields**:
  - `firmware`: The firmware being assigned.
  - `device`, `module`, `inventory_item`: The hardware receiving the firmware.
  - `ticket_number`, `patch_date`, `comment`: Metadata for the assignment.

## Relationships
- Firmware objects are linked to hardware types (e.g., devices, modules) via foreign keys.
- FirmwareAssignment objects link firmware to specific hardware instances.

## Constraints
- Only one hardware type (device, module, or inventory item) can be set for a firmware or assignment.
- Unique constraints ensure no duplicate firmware or assignments exist.