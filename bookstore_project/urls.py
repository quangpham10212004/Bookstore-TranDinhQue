from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('catalog/', include('catalog.urls')),
    path('sales/', include('sales.urls')),
    path('', include('catalog.urls')), # Home page is in catalog
]
