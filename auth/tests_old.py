from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.
class APIAuthTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.client = APIClient()
		cls.user = get_user_model().objects.create_user(username="test1", email="test1@example.com", first_name="test", last_name="user1", password="micknmouse1")
	
	def test_register_user_api(self):
		response = self.client.post("/api/auth/register/", {
			"username": "test",
			"email": "test@example.com",
			"first_name": "test",
			"last_name": "user",
			"password": "micknmouse1"
		})

		data = response.json()
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(data["user"]["first_name"], get_user_model().objects.get(username=data["user"]["username"]).first_name)
		self.assertIn("token", data)
		self.assertIn("refresh", data)
	
	def test_login_user_api(self):
		response = self.client.post("/api/auth/login/", {
			"email": "test1@example.com",
			"password": "micknmouse1"
		})

		data = response.json()
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(data["user"]["first_name"], get_user_model().objects.get(username=data["user"]["username"]).first_name)
		self.assertIn("access", data)
		self.assertIn("refresh", data)
