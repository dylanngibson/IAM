from django.urls import path
from .views import CustomAuthToken, LogoutView

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
]
