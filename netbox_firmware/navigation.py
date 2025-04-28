from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton, get_plugin_config

firmware_buttons = [
    PluginMenuButton(
        link='plugins:netbox_firmware:firmware_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["netbox_firmware.add_firmware"],
    ),
    PluginMenuButton(
        link='plugins:netbox_firmware:firmware_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        permissions=["netbox_firmware.import_firmware"],
    ),
]
firmware_assignments_buttons = [
    PluginMenuButton(
        link='plugins:netbox_firmware:firmwareassignment_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["netbox_firmware.add_firmware_assignment"],
    ),
    PluginMenuButton(
        link='plugins:netbox_firmware:firmwareassignment_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        permissions=["netbox_firmware.aimport_firmware_assignment"],
    ),
]
firmware_items = (
    PluginMenuItem(
        link='plugins:netbox_firmware:firmware_list',
        link_text='Firmwares',
        permissions=["netbox_firmware.view_firmware"],
        buttons= firmware_buttons,
    ),
    PluginMenuItem(
        link='plugins:netbox_firmware:firmwareassignment_list',
        link_text='Firmware Assignments',
        permissions=["netbox_firmware.view_firmware_assignment"],
        buttons= firmware_assignments_buttons,
    ),
)

bios_buttons = [
    PluginMenuButton(
        link='plugins:netbox_firmware:bios_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["netbox_firmware.add_bios"],
    ),
    PluginMenuButton(
        link='plugins:netbox_firmware:bios_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        permissions=["netbox_firmware.import_bios"],
    ),
]
bios_assignments_buttons = [
    PluginMenuButton(
        link='plugins:netbox_firmware:biosassignment_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["netbox_firmware.add_bios_assignment"],
    ),
    PluginMenuButton(
        link='plugins:netbox_firmware:biosassignment_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        permissions=["netbox_firmware.import_bios_assignment"],
    ),
]
bios_items = (
    PluginMenuItem(
        link='plugins:netbox_firmware:bios_list',
        link_text='BIOS',
        permissions=["netbox_firmware.view_bios"],
        buttons= bios_buttons,
    ),
    PluginMenuItem(
        link='plugins:netbox_firmware:biosassignment_list',
        link_text='BIOS Assignments',
        permissions=["netbox_firmware.view_bios_assignment"],
        buttons= bios_assignments_buttons,
    ),
)

if get_plugin_config('netbox_firmware', 'top_level_menu'):
    menu = PluginMenu(
        label=f'Firmwares',
        groups=(
            ('Firmware', firmware_items),
            ('BIOS', bios_items),
        ),
        icon_class = 'mdi mdi-clipboard-text-multiple-outline'
    )
else:
    menu_items = firmware_items + bios_items