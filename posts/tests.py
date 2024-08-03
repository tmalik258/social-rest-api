import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Post

# Create your tests here.

class APIPostTest(TestCase):
	"""
	Create `Post`
	"""
	@classmethod
	def setUpTestData(cls) -> None:
		cls.user = get_user_model().objects.create_user(
			username='micky',
			email='micky@example.com',
			password='micknmouse1'
		)
		cls.post = Post.objects.create(
			author=cls.user,
			body="A simple but complex post"
		)

	def setUp(self) -> None:
		self.client = APIClient()
		self.user_id = None
		self.access_token = None

	def get_access_token(self):
		if not self.access_token:
			response = self.client.post('/api/auth/login/', {
				"email": "micky@example.com",
				"password": "micknmouse1"
			})
		
			self.assertEqual(response.status_code, status.HTTP_200_OK)

			data: dict = response.json()

			self.assertIn("access", data)
			self.assertIn("user", data)
			self.assertIn("id", data["user"])

			self.user_id = data["user"]["id"]
			self.access_token = data["access"]
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

	def test_get_posts_list(self):
		response = self.client.get('/api/posts/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_post_obj(self):
		response = self.client.get(f'/api/posts/{self.post.public_id}/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_post_obj(self):
		self.get_access_token()
		
		response = self.client.post('/api/posts/', {
			"author": self.user_id,
			"body": "A simple post"
		})

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_post_obj(self):
		self.get_access_token()

		response = self.client.put(f'/api/posts/{self.post.public_id}/', {
			"author": self.user_id,
			"body": "A simple but complex post (edited)"
		})

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		data = response.json()

		self.assertTrue(data["edited"])
	
	def test_delete_post_obj(self):
		self.get_access_token()

		response = self.client.delete(f"/api/posts/{self.post.public_id}/")

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
	
	def test_like_post(self):
		self.get_access_token()

		response = self.client.post(f'/api/posts/{self.post.public_id}/like/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
		data = response.json()

		self.assertEqual(data["likes_count"], 1)
		self.assertEqual(data["liked"], True)
	
	def test_unlike_post(self):
		self.get_access_token()

		# like the post first and test if it is liked
		response = self.client.post(f'/api/posts/{self.post.public_id}/like/')
		
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		data = response.json()
		self.assertEqual(data["likes_count"], 1)
		
		# remove the like from the post and test if it is unliked
		response = self.client.post(f'/api/posts/{self.post.public_id}/remove_like/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
		data = response.json()

		self.assertEqual(data["likes_count"], 0)
