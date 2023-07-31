from django.urls import path
from . import views

urlpatterns = [
    path('upload_vehicle_data/', views.upload_vehicle_data, name='upload_vehicle_data'),
]