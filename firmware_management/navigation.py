from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton, get_plugin_config

firmware_buttons = [
    PluginMenuButton(
        link='plugins:firmware_management:firmware_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["firmware_management.add_firmware"],
    ),
]
firmware_items = (
    PluginMenuItem(
        link='plugins:firmware_management:firmware_list',
        link_text='Firmware',
        permissions=["firmware_management.view_firmware"],
        buttons= firmware_buttons,
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