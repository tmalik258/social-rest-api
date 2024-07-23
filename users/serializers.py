from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
	# created = serializers.DateTimeField(read_only=True)
	

	class Meta:
		model = get_user_model()
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'is_active', 'created', 'updated')
		read_only_field = ['is_active', 'created', 'updated']