from django.urls import path

from . import views

urlpatterns = [
    # Test List 
    path('firmware/', views.TestView.as_view(), name='test_view'),
]