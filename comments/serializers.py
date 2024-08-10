from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from abstract.serializers import AbstractSerializer
from comments.models import Comment
from posts.models import Post
from users.serializers import UserSerializer


class CommentSerializer(AbstractSerializer):
	author = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field='public_id')
	post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='public_id')

	def validate_author(self, value):
		if self.context["request"].user != value:
			raise ValidationError("You can't create a post for another user")
		return value
	
	def validate_post(self, value):
		if self.instance:
			return self.instance.post
		return value
	
	def update(self, instance, validated_data):
		if not instance.edited:
			validated_data["edited"] = True
		
		instance = super().update(instance, validated_data)

		return instance

	def to_representation(self, instance):
		rep = super().to_representation(instance)
		author = get_user_model().objects.get_object_by_public_id(rep["author"])
		rep["author"] = UserSerializer(author).data

		return rep
	
	class Meta:
		model = Comment
		# List of all the fields that can be included in a request or a response
		fields = ['id', 'post', 'author', 'body', 'edited', 'created', 'updated']
		read_only_fields = ['edited', 'created', 'updated']