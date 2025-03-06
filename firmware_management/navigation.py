from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton, get_plugin_config

firmware_buttons = [
    PluginMenuButton(
        link='plugins:firmware_management:firmware_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["firmware_management.add_firmware"],
    ),
]
firmware_assignments_buttons = [
    PluginMenuButton(
        link='plugins:firmware_management:firmwareassignment_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["firmware_management.add_firmware_assignment"],
    ),
]
firmware_items = (
    PluginMenuItem(
        link='plugins:firmware_management:firmware_list',
        link_text='Firmware',
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

if get_plugin_config('firmware_management', 'top_level_menu'):
    menu = PluginMenu(
        label=f'Firmwares',
        groups=(
            ('Firmware', firmware_items),
        ),
        icon_class = 'mdi mdi-clipboard-text-multiple-outline'
    )
else:
    menu_items = firmware_items