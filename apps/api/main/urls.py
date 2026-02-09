from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/users/', include('urls.users')),
    path('api/vehicles/', include('urls.vehicles')),
    # path('api/checklists/', include('urls.checklists')),
]
