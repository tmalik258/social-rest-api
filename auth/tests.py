from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.
class APIAuthTest(TestCase):
	@classmethod
	def setUpTestData(cls) -> None:
		cls.client = APIClient()
	
	def test_register_user_api(self):
		response = self.client.post("api/register")