from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
    path('add/', views.add_user, name='add-user'),
    path('<str:nombre_usuario>/', views.user_profile, name='user-profile'),
    path('<str:nombre_usuario>/del/', views.del_user, name='del-user'),
]
