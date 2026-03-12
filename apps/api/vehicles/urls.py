from django.urls import path

from . import views

app_name = 'vehicles'


urlpatterns = [
    path('', views.vehicle_list, name='vehicle-list'),
    path('add/', views.add_vehicle, name='add-vehicle'),
    path('<str:matricula>/del/', views.del_vehicle, name='del-vehicle'),
    path(
        '<str:matricula>/change_vehicle_image/',
        views.change_vehicle_image,
        name='change-vehicle-image',
    ),
]
