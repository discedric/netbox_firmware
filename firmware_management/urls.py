from django.urls import include, path

from utilities.urls import get_model_urls
from . import views

urlpatterns = [
    # Firmwares
    path('firmwares/', include(get_model_urls('firmware_management', 'firmware', detail=False))),
    path('firmwares/<int:pk>/', include(get_model_urls('firmware_management', 'firmware'))),
]