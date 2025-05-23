# Generated by Django 5.1.6 on 2025-04-28 13:52

import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dcim', '0200_populate_mac_addresses'),
        ('extras', '0122_charfield_null_choices'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=255)),
                ('file_name', models.CharField(blank=True, max_length=255, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='bios-files')),
                ('status', models.CharField(default='active', max_length=50)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('device_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bios', to='dcim.devicetype')),
                ('module_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bios', to='dcim.moduletype')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'BIOS',
                'verbose_name_plural': 'BIOS',
                'ordering': ('name', 'device_type', 'module_type'),
            },
        ),
        migrations.CreateModel(
            name='BiosAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('description', models.TextField(blank=True, null=True)),
                ('ticket_number', models.CharField(blank=True, max_length=100, null=True)),
                ('patch_date', models.DateField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('bios', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='BiosAssignment', to='netbox_firmware.bios')),
                ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='BiosAssignment', to='dcim.device')),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='BiosAssignment', to='dcim.module')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'BIOS Assignment',
                'verbose_name_plural': 'BIOS Assignments',
                'ordering': ('bios', 'device', 'module'),
            },
        ),
        migrations.CreateModel(
            name='Firmware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=255)),
                ('file_name', models.CharField(blank=True, max_length=255, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='firmware-files')),
                ('status', models.CharField(default='active', max_length=50)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('device_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='firmware', to='dcim.devicetype')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='firmware', to='dcim.manufacturer')),
                ('module_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='firmware', to='dcim.moduletype')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Firmware',
                'verbose_name_plural': 'Firmwares',
                'ordering': ('name', 'device_type', 'module_type', 'manufacturer'),
            },
        ),
        migrations.CreateModel(
            name='FirmwareAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('description', models.TextField(blank=True, null=True)),
                ('ticket_number', models.CharField(blank=True, max_length=100, null=True)),
                ('patch_date', models.DateField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='FirmwareAssignment', to='dcim.device')),
                ('device_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='FirmwareAssignment', to='dcim.devicetype')),
                ('firmware', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='FirmwareAssignment', to='netbox_firmware.firmware')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='FirmwareAssignment', to='dcim.manufacturer')),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='FirmwareAssignment', to='dcim.module')),
                ('module_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='FirmwareAssignment', to='dcim.moduletype')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Firmware Assignment',
                'verbose_name_plural': 'Firmware Assignments',
                'ordering': ('firmware', 'device', 'module'),
            },
        ),
        migrations.AddConstraint(
            model_name='bios',
            constraint=models.CheckConstraint(condition=models.Q(('device_type__isnull', False), ('module_type__isnull', False), _connector='OR'), name='bios_device_type_or_module_type_required'),
        ),
        migrations.AlterUniqueTogether(
            name='bios',
            unique_together={('name', 'device_type', 'module_type')},
        ),
        migrations.AddConstraint(
            model_name='biosassignment',
            constraint=models.CheckConstraint(condition=models.Q(('device__isnull', False), ('module__isnull', False), _connector='OR'), name='bios_device_or_module_required'),
        ),
        migrations.AddConstraint(
            model_name='firmware',
            constraint=models.CheckConstraint(condition=models.Q(('device_type__isnull', False), ('module_type__isnull', False), _connector='OR'), name='firmware_either_device_type_or_module_type_required'),
        ),
        migrations.AlterUniqueTogether(
            name='firmware',
            unique_together={('name', 'manufacturer', 'device_type', 'module_type')},
        ),
        migrations.AddConstraint(
            model_name='firmwareassignment',
            constraint=models.CheckConstraint(condition=models.Q(('device__isnull', False), ('module__isnull', False), _connector='OR'), name='firmassign_either_device_or_module_required'),
        ),
        migrations.AddConstraint(
            model_name='firmwareassignment',
            constraint=models.CheckConstraint(condition=models.Q(('device_type__isnull', False), ('module_type__isnull', False), _connector='OR'), name='firmassign_either_device_type_or_module_type_required'),
        ),
    ]
