from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
    path('add/', views.add_user, name='add-user'),
    path('perfil/<str:nombre_usuario>/', views.user_profile, name='user-profile'),
    path('perfil/<str:nombre_usuario>/mod/', views.mod_profile, name='mod-profile'),
    path('perfil/<str:nombre_usuario>/del/', views.del_user, name='del-user'),
]
