from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

class APIUsersTest(TestCase):
	"""
	Account Retrieve
	"""

	@classmethod
	def setUpTestData(cls) -> None:
		cls.user = get_user_model().objects.create_user(
			username='talha',
			email='talha@example.com',
			password='outlook25'
		)
	
	def test_retrieve_users_list(self):
		"""
		Retrieve List of `User` objects
		"""
		response = self.client.get('/api/users/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		data = response.data
		self.assertEqual(data[0]["username"], 'talha')

		User = get_user_model()
		self.assertTrue(User.objects.filter(username='talha').exists())
	
	def test_retrieve_user_object(self):
		"""
		Retrieve `User` object
		"""
		response = self.client.get(f'/api/users/{self.user.public_id}/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		data = response.data
		self.assertEqual(data['username'], 'talha')
		self.assertEqual(data['email'], 'talha@example.com')

	def test_patch_user_object(self):
		"""
		Patch/Update `User` object
		"""
		response = self.client.patch(f'/api/users/{self.user.public_id}/', {
			"first_name": "Talha"
		})

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)