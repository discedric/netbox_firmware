from django.urls import include, path

from utilities.urls import get_model_urls
from . import views

urlpatterns = [
    # Firmwares
    path('firmwares/', include(get_model_urls('firmware_management', 'firmware', detail=False))),
    path('firmwares/<int:pk>/', include(get_model_urls('firmware_management', 'firmware'))),
    path('firmwares/<int:pk>/changelog/', views.FirmwareChangeLogView.as_view(), name='firmware_changelog'),
    
    # Assignments
    path('Assignment/', include(get_model_urls('firmware_management','firmwareassignment',detail=False))),
    path('Assignment/<int:pk>/', include(get_model_urls('firmware_management', 'firmwareassignment'))),
    path('Assignment/<int:pk>/changelog/', views.FirmwareAssignmentChangeLogView.as_view(), name='firmwareassignment_changelog'),
]