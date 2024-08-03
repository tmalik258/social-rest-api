from django.db import models
from django.conf import settings

from abstract.models import AbstractManager, AbstractModel

# Create your models here.

class PostManager(AbstractManager):
	pass


class Post(AbstractModel):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	body = models.TextField()
	edited = models.BooleanField(default=False)

	objects = PostManager()

	def __str__(self) -> str:
		return f"{self.author.name}"
