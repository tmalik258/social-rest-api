import pytest

from rest_framework import status

from fixtures.user import user


class TestAuthenticationViewSet:
	endpoint = '/api/auth/'

	def test_login(self, client, user):
		data = {
			"username": user.username,
			"password": "test_password"
		}

		response = client.post(f"{self.endpoint}login/", data)

		assert response.status_code == status.HTTP_200_OK
		assert response.data['access']
		assert response.data['user']['id'] == user.public_id.hex
		assert response.data['user']['username'] == user.username
		assert response.data['user']['email'] == user.email
	
	@pytest.mark.django_db
	def test_register(self, client):
		data = {
			"username": "tmalik",
			"email": "tmalik@example.com",
			"first_name": "Talha",
			"last_name": "Malik",
			"password": "test_password"
		}

		response = client.post(f"{self.endpoint}register/", data)

		assert response.status_code == status.HTTP_201_CREATED
		assert response.data['user']['username'] == data['username']
		assert response.data['user']['email'] == data['email']
	
	def test_refresh(self, client, user):
		data = {
			"username": user.username,
			"password": "test_password"
		}

		response = client.post(f'{self.endpoint}login/', data)

		assert response.status_code == status.HTTP_200_OK

		data_refresh = {
			"refresh": response.data["refresh"]
		}

		response = client.post(f'{self.endpoint}refresh/', data_refresh)

		assert response.status_code == status.HTTP_200_OK
		assert response.data["access"]