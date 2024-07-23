import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# Create your models here.

class UserManager(BaseUserManager):
	"""
	Methods to create a user and a superuser
	"""
	def get_object_by_public_id(self, public_id):
		try:
			instance = self.get(public_id=public_id)
			return instance
		except (ObjectDoesNotExist, ValueError, TypeError):
			return Http404
	
	def create_user(self, username, email, password=None, **kwargs):
		"""
		Create and return a `User` with an email, username and password.
		"""
		if username is None:
			raise TypeError('User must have a username.')
		if email is None:
			raise TypeError('User must have an email.')
		if password is None:
			raise TypeError('User must have a password.')

		user = self.model(username=username, email=self.normalize_email(email), **kwargs)
		user.set_password(password)
		user.save(using=self._db)

		return user
	
	def create_superuser(self, username, email, password=None, **kwargs):
		"""
 		Create and return a `User` with superuser (admin) permissions.
		"""
		if password is None:
			raise TypeError('SuperUser must have a password.')
		if email is None:
			raise TypeError('SuperUser must have an email.')
		if username is None:
			raise TypeError('SuperUser must have a username.')
		
		user = self.create_user(username, email, password, **kwargs)
		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db)

		return user



class User(AbstractBaseUser, PermissionsMixin):
	"""
	Custom User Model to include custom fields
	"""
	public_id = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False)
	username = models.CharField(db_index=True, max_length=255, unique=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(db_index=True, unique=True)
	bio = models.TextField(blank=True, null=True)
	is_active = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = UserManager()

	def __str__(self) -> str:
		return self.email

	@property
	def name(self):
		return f"{self.first_name} {self.last_name}"
	