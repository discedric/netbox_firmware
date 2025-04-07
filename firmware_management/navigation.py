from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton, get_plugin_config

firmware_buttons = [
    PluginMenuButton(
        link='plugins:firmware_management:firmware_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["firmware_management.add_firmware"],
    ),
    PluginMenuButton(
        link='plugins:firmware_management:firmware_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        permissions=["firmware_management.import_firmware"],
    ),
]
firmware_assignments_buttons = [
    PluginMenuButton(
        link='plugins:firmware_management:firmwareassignment_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["firmware_management.add_firmware_assignment"],
    ),
    PluginMenuButton(
        link='plugins:firmware_management:firmwareassignment_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        permissions=["firmware_management.aimport_firmware_assignment"],
    ),
]
firmware_items = (
    PluginMenuItem(
        link='plugins:firmware_management:firmware_list',
        link_text='Firmwares',
        permissions=["firmware_management.view_firmware"],
        buttons= firmware_buttons,
    ),
    PluginMenuItem(
        link='plugins:firmware_management:firmwareassignment_list',
        link_text='Firmware Assignments',
        permissions=["firmware_management.view_firmware_assignment"],
        buttons= firmware_assignments_buttons,
    ),
)

bios_buttons = [
    PluginMenuButton(
        link='plugins:firmware_management:bios_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["firmware_management.add_bios"],
    ),
    PluginMenuButton(
        link='plugins:firmware_management:bios_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        permissions=["firmware_management.import_bios"],
    ),
]
bios_assignments_buttons = [
    PluginMenuButton(
        link='plugins:firmware_management:biosassignment_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["firmware_management.add_bios_assignment"],
    ),
    PluginMenuButton(
        link='plugins:firmware_management:biosassignment_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        permissions=["firmware_management.import_bios_assignment"],
    ),
]
bios_items = (
    PluginMenuItem(
        link='plugins:firmware_management:bios_list',
        link_text='BIOS',
        permissions=["firmware_management.view_bios"],
        buttons= bios_buttons,
    ),
    PluginMenuItem(
        link='plugins:firmware_management:biosassignment_list',
        link_text='BIOS Assignments',
        permissions=["firmware_management.view_bios_assignment"],
        buttons= bios_assignments_buttons,
    ),
)

if get_plugin_config('firmware_management', 'top_level_menu'):
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