from django.urls import include, path

from utilities.urls import get_model_urls
from netbox.views.generic import ObjectChangeLogView
from . import views

urlpatterns = [
    # Firmwares
    path('firmwares/', include(get_model_urls('netbox_firmware', 'firmware', detail=False))),
    path('firmwares/<int:pk>/', include(get_model_urls('netbox_firmware', 'firmware'))),
    
    # Assignments
    path('assignment/', include(get_model_urls('netbox_firmware','firmwareassignment',detail=False))),
    path('assignment/<int:pk>/', include(get_model_urls('netbox_firmware', 'firmwareassignment'))),
    
    # Bios
    path('bios/', include(get_model_urls('netbox_firmware', 'bios', detail=False))),
    path('bios/<int:pk>/', include(get_model_urls('netbox_firmware', 'bios'))),
    
    # Bios Assignments
    path('biosassignment/', include(get_model_urls('netbox_firmware','biosassignment',detail=False))),
    path('biosassignment/<int:pk>/', include(get_model_urls('netbox_firmware', 'biosassignment'))),
]