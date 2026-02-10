from django.urls import path

from . import views

app_name = 'vehicles'


urlpatterns = [
    path('', views.vehicle_list, name='vehicle-list'),
    path('add/', views.add_vehicle, name='add-vehicle'),
]
