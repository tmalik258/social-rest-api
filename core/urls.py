from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import SimpleRouter

from users.viewsets import UserViewSet

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
	path('api/', include(router.urls)),
]
