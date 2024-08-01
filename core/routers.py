from rest_framework import routers
# from auth.viewsets.login import LoginViewSet
# from auth.viewsets.refresh import RefreshViewSet
from auth.viewsets import (LoginViewset, RegisterViewSet, RefreshViewSet)

from users.viewsets import UserViewSet

router = routers.SimpleRouter()


# ##################################################################### #
# ############################### USER ################################ #
# ##################################################################### #

router.register(r'user', UserViewSet, basename='user')


# ##################################################################### #
# ############################### AUTH ################################ #
# ##################################################################### #

router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewset, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')




urlpatterns = [
	*router.urls,
]