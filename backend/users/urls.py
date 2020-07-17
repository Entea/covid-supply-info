from django.urls import path, include

from users.views import LogoutView

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('logout/', LogoutView.as_view(), name='logout_view')
]
