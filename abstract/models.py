import uuid

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class AbstractManager(models.Manager):
	"""
	Abstract Model Manager for abstract methods
	"""
	def get_object_by_public_id(self, public_id):
		try:
			instance = self.get(public_id=public_id)
			return instance
		except (ObjectDoesNotExist, ValueError, TypeError):
			return Http404


class AbstractModel(models.Model):
	"""
	Abstract model for abstract attributes and methods
	"""
	public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	objects = AbstractManager()

	class Meta:
		abstract = True