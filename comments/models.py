from django.db import models
from django.conf import settings

from abstract.models import AbstractManager, AbstractModel

# Create your models here.
class CommentManager(AbstractManager):
	pass

class Comment(AbstractModel):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	post = models.ForeignKey('posts.Post', on_delete=models.PROTECT)
	body = models.TextField()
	edited = models.BooleanField(default=False)

	objects = CommentManager()

	def __str__(self) -> str:
		return self.author.name