from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from comments.models import Comment
from posts.models import Post
# Create your tests here.

class APICommentTest(TestCase):
	"""
	Create `Comment`
	"""
	@classmethod
	def setUpTestData(cls) -> None:
		cls.user = get_user_model().objects.create_user(
			username='micky',
			email='micky@example.com',
			password='micknmouse1'
		)

		cls.test_user = get_user_model().objects.create_user(
			username='test',
			email='test@example.com',
			password='testnsolve1'
		)

		cls.post: Post = Post.objects.create(
			author=cls.user,
			body="A simple but complex post"
		)

		cls.comment: Comment = Comment.objects.create(
			author=cls.user,
			post=cls.post,
			body="A simple comment"
		)
	
	def setUp(self) -> None:
		self.client = APIClient()
		self.user_id = None
		self.access_token = None
	
	def get_access_token(self):
		"""
		Get user_id, access_token, if not already. Authorized the client so requests can be made.
		"""
		if not self.access_token:
			response = self.client.post('/api/auth/login/', {
				"email": "micky@example.com",
				"password": "micknmouse1"
			})

			self.assertEqual(response.status_code, status.HTTP_200_OK)

			data: dict = response.json()

			self.assertIn("user", data)
			self.assertIn("access", data)
			self.assertIn("id", data["user"])

			self.user_id = data["user"]["id"]
			self.access_token = data["access"]

		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
	
	def test_retrieve_comments_list(self):
		"""
		Retrieve lists of `Comment` using post_id only
		"""
		self.get_access_token()

		response = self.client.get(f'/api/posts/{self.post.public_id}/comments/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_retrieve_comment_object(self):
		"""
		Retrieve `Comment` object using post_id and comment_id
		"""
		self.get_access_token()

		response = self.client.get(f'/api/posts/{self.post.public_id}/comments/{self.comment.public_id}/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_create_comment(self):
		"""
		Create `Comment` object
		"""
		self.get_access_token()

		response = self.client.post(f'/api/posts/{self.post.public_id}/comments/', {
			"author": self.user_id,
			"body": "Hey! I like your post.",
			"post": self.post.public_id
		})

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		data: dict = response.json()

		self.assertIn("Hey! I like your post.", data["body"])
	
	def test_create_comment_validation_error(self):
		"""
		Check whether validation error is raised or not when a `User` creates `Comment` for another `User`
		"""
		self.get_access_token()

		response = self.client.post(f'/api/posts/{self.post.public_id}/comments/', {
			"author": self.test_user.public_id,
			"body": "Hey! I like your post.",
			"post": self.post.public_id
		})

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		data = response.json()

		self.assertIn("author", data)
		self.assertEqual(data["author"][0], "You can't create a post for another user")
	
	def test_patch_comment(self):
		"""
		Patch/Update `Comment` object using post_id and comment_id
		"""
		self.get_access_token()

		response = self.client.put(f'/api/posts/{self.post.public_id}/comments/{self.comment.public_id}/', {
			"author": self.user_id,
			"post": self.post.public_id,
			"body": "Hey! I dont't like your post. (edited)"
		})

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		data: dict = response.json()

		self.assertIn("(edited)", data["body"])
		self.assertTrue(data["edited"])
	
	def test_delete_comment(self):
		"""
		Delete `Comment` object using post_id and comment_id
		"""
		self.get_access_token()

		response = self.client.delete(f'/api/posts/{self.post.public_id}/comments/{self.comment.public_id}/')

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
