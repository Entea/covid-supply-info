from django.urls import path, include

urlpatterns = [
    path('auth/', include('rest_auth.urls'))
]
