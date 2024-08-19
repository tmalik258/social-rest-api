from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from abstract.models import AbstractManager, AbstractModel

# Create your models here.

class UserManager(BaseUserManager, AbstractManager):
	"""
	Methods to create a user and a superuser
	"""
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



class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
	"""
	Custom User Model to include custom fields
	"""
	username = models.CharField(db_index=True, max_length=255, unique=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(db_index=True, unique=True)
	bio = models.TextField(blank=True, null=True)
	is_active = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)
	posts_liked = models.ManyToManyField("posts.Post", related_name="liked_by")
	
	USERNAME_FIELD = 'username'
	EMAIL_FIELD  = 'email'

	objects = UserManager()

	def __str__(self) -> str:
		return self.email
	
	def like(self, post):
		"""
		Like `post` if it hasn't been done yet.
		"""
		return self.posts_liked.add(post)

	def unlike(self, post):
		"""
		Remove a like from `post`
		"""
		return self.posts_liked.remove(post)
	
	def has_liked(self, post):
		"""
		Return True if the `user` has liked a `post`; else False
		"""
		return self.posts_liked.filter(pk=post.pk).exists()

	@property
	def name(self):
		return f"{self.first_name} {self.last_name}"
	
