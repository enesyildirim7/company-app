from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Business Management API",
      default_version='v1',
      description="Kuruluş kayıt ve yönetim uygulaması.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="bilgi@sd.com.tr"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Dökümantasyon
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API endpoints
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls",namespace="users")),
    path("api/v1/company/", include("company.urls",namespace="company")),
]
