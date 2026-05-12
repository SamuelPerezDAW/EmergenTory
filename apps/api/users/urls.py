from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
    path('', views.list_users, name='list-users'),
    path('add/', views.add_user, name='add-user'),
    path('profile/<str:nombre_usuario>/', views.user_profile, name='user-profile'),
    path('profile/<str:nombre_usuario>/mod/', views.mod_profile, name='mod-profile'),
    path('profile/<str:nombre_usuario>/del/', views.del_user, name='del-user'),
    path(
        'profile/<str:nombre_usuario>/reset-password/', views.reset_password, name='reset-password'
    ),
]
