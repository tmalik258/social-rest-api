from django.contrib.auth import get_user_model

from abstract.serializers import AbstractSerializer


class UserSerializer(AbstractSerializer):
	class Meta:
		model = get_user_model()
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'is_active', 'created', 'updated')
		read_only_field = ['is_active', 'created', 'updated']