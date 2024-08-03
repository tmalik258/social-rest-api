from django.contrib.auth import get_user_model

from rest_framework import permissions

from abstract.viewsets import AbstractViewSet
from users.serializers import UserSerializer

# Create your views here.

class UserViewSet(AbstractViewSet):
	http_method_names = ('patch', 'get')
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = UserSerializer
	
	def get_queryset(self):
		if self.request.user.is_superuser:
			return get_user_model().objects.all()
		return get_user_model().objects.exclude(is_superuser=True)
	
	def get_object(self):
		obj = get_user_model().objects.get_object_by_public_id(self.kwargs['pk'])
		self.check_object_permissions(self.request, obj)
		return obj