# Templates Documentation

The `templates` directory contains HTML templates for rendering firmware and BIOS-related views. These templates define the structure and layout of the plugin's user interface.

## Key Templates

### firmware.html
- **Purpose**: Displays details of a firmware object.
- **Includes**: Information about the firmware's name, status, file, and associated hardware.

### firmwareassignment.html
- **Purpose**: Displays details of a firmware assignment.
- **Includes**: Metadata like ticket number, patch date, and the hardware receiving the firmware.

### inc/firmware_info.html
- **Purpose**: Renders a panel showing firmware information assigned to a device, module, or inventory item.

### inc/firmware_stats_counts.html
- **Purpose**: Displays statistics about firmware counts related to a manufacturer.

## Usage
These templates are used in conjunction with views to render data dynamically. They leverage Django's template language for logic and formatting.