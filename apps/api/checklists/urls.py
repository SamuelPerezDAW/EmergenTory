from django.urls import path

from . import views

app_name = 'checklists'


urlpatterns = [
    path('', views.checklists_list, name='checklists-list'),
    path('checkitems/', views.checkitems_list, name='checkitems-list'),
    path('checkitems/add/', views.add_item, name='add-item'),
    path('checkitems/mod/', views.mod_item, name='mod-item'),
    path('checkitems/del/', views.del_item, name='del-item'),
]
