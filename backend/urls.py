from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # — API Endpoints —
    path('api/auth/', include('auth_app.urls')),           # /api/auth/login/, /api/auth/logout/, etc.
    path('api/roles/', include('roles.urls')),              # /api/roles/, /api/roles/<pk>/, /api/roles/<pk>/set_permissions/, etc.
    path('api/attributes/', include('attributes.urls')),    # /api/attributes/, /api/users/<id>/attributes/, etc.
    path('api/alerts/', include('alerts.urls')),            # /api/alerts/recent/, /api/alerts/unseen-count/, etc.
    path('api/users/', include('users.urls')),              # /api/users/, /api/users/me/, /api/users/<pk>/, etc.
]
