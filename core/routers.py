from rest_framework_nested import routers

from auth.viewsets import (LoginViewset, RegisterViewSet, RefreshViewSet)

from comments.viewsets import CommentViewSet
from posts.viewsets import PostViewSet
from users.viewsets import UserViewSet

router = routers.SimpleRouter()


# ##################################################################### #
# ############################### USER ################################ #
# ##################################################################### #

router.register(r'users', UserViewSet, basename='user')


# ##################################################################### #
# ############################### AUTH ################################ #
# ##################################################################### #

router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewset, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')


# ##################################################################### #
# ############################### POST and COMMENT ################################ #
# ##################################################################### #

router.register(r'posts', PostViewSet, basename='post')

posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comment')

urlpatterns = [
	*router.urls,
	*posts_router.urls,
]