from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('roles/', include('roles.urls')),
    path('auth/', include('auth_app.urls')),
    path("api/", include("roles.urls")),
    path("api/", include("attributes.urls")),
    path("api/alerts/", include("alerts.urls")),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # ✅ this matches your frontend
]
