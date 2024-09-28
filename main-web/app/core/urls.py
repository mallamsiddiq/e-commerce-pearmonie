from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

url_version = "api/v1"
urlpatterns = [
    path(f"{url_version}/schema/", SpectacularAPIView.as_view(), name='schema'),
    path(f"{url_version}/doc/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(f"{url_version}/redoc/", SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path(f"{url_version}/", include('authapp.urls')),
    path(f"{url_version}/", include('store.urls')),
]