from django.urls import include, path

from utilities.urls import get_model_urls
from . import views

urlpatterns = [
    # Firmwares
    path('firmwares/', include(get_model_urls('firmware_management', 'firmware', detail=False))),
    path('firmwares/<int:pk>/', include(get_model_urls('firmware_management', 'firmware'))),
    path('firmwares/<int:pk>/changelog/', views.FirmwareChangeLogView.as_view(), name='firmware_changelog'),
    path('firmwares/<int:pk>/journal/', views.FirmwareJournalView.as_view(), name='firmware_journal'),

    path('device/<int:device_id>/reassign/', views.FirmwareDeviceReassignView.as_view(), name='firmware_device_reassign'),
    path('module/<int:module_id>/reassign/', views.FirmwareModuleReassignView.as_view(), name='firmware_module_reassign'),
    
    # Assignments
    path('assignment/', include(get_model_urls('firmware_management','firmwareassignment',detail=False))),
    path('assignment/<int:pk>/', include(get_model_urls('firmware_management', 'firmwareassignment'))),
    path('assignment/<int:pk>/changelog/', views.FirmwareAssignmentChangeLogView.as_view(), name='firmwareassignment_changelog'),
    path('assignment/<int:pk>/journal/', views.FirmwareAssignmentJournalView.as_view(), name='firmwareassignment_journal'),
    
    # Bios
    path('bios/', include(get_model_urls('firmware_management', 'bios', detail=False))),
    path('bios/<int:pk>/', include(get_model_urls('firmware_management', 'bios'))),
    path('bios/<int:pk>/changelog/', views.BiosChangeLogView.as_view(), name='bios_changelog'),
    path('bios/<int:pk>/journal/', views.BiosJournalView.as_view(), name='bios_journal'),
    
    # Bios Assignments
    path('biosassignment/', include(get_model_urls('firmware_management','biosassignment',detail=False))),
    path('biosassignment/<int:pk>/', include(get_model_urls('firmware_management', 'biosassignment'))),
    path('biosassignment/<int:pk>/changelog/', views.BiosAssignmentChangeLogView.as_view(), name='biosassignment_changelog'),
    path('biosassignment/<int:pk>/journal/', views.BiosAssignmentJournalView.as_view(), name='biosassignment_journal'),
]