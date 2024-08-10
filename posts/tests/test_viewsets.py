from rest_framework import status

from fixtures.user import user
from fixtures.post import post


class TestPostViewSet:
	endpoint = '/api/posts/'

	def test_list(self, client, user, post):
		client.force_authenticate(user=user)

		response = client.get(self.endpoint)

		assert response.status_code == status.HTTP_200_OK
		assert response.data["count"] == 1
	
	def test_retrieve(self, client, user, post):
		client.force_authenticate(user=user)

		response = client.get(f'{self.endpoint}{post.public_id}/')

		assert response.status_code == status.HTTP_200_OK
		assert response.data['id'] == post.public_id.hex
		assert response.data['body'] == post.body
		assert response.data['author']['id'] == post.author.public_id.hex

	def test_create(self, client, user, post):
		client.force_authenticate(user=user)

		data = {
			"author": user.public_id.hex,
			"body": "Test Post Body"
		}

		response = client.post(f'{self.endpoint}', data)

		assert response.status_code == status.HTTP_201_CREATED
		assert response.data["body"] == data['body']
		assert response.data["author"]['id'] == user.public_id.hex
	
	def test_update(self, client, user, post):
		client.force_authenticate(user=user)

		data = {
			"author": user.public_id.hex,
			"body": "Test Post Body (updated)"
		}

		response = client.put(f'{self.endpoint}{(post.public_id)}/', data)

		assert response.status_code == status.HTTP_200_OK
		assert response.data["body"] == data["body"]
		assert response.data['edited']
	
	def test_delete(self, client, user, post):
		client.force_authenticate(user=user)

		response = client.delete(f'{self.endpoint}{post.public_id}/')

		assert response.status_code == status.HTTP_204_NO_CONTENT
	
	def test_list_anonymous(self, client, post):
		response = client.get(self.endpoint)

		assert response.status_code == status.HTTP_200_OK
		assert response.data['count'] == 1
	
	def test_retrieve_anonymous(self, client, post):
		response = client.get(f'{self.endpoint}{post.public_id}/')

		assert response.status_code == status.HTTP_200_OK
		assert response.data['id'] == post.public_id.hex
		assert response.data['body'] == post.body
		assert response.data['author']['id'] == post.author.public_id.hex
	
	def test_create_anonymous(self, client):
		data = {
			"body": "Test Post Body",
			"author": "test_user"
		}

		response = client.post(self.endpoint, data)

		assert response.status_code == status.HTTP_401_UNAUTHORIZED
	
	def test_update_anonymous(self, client, post):
		data = {
			"author": "test_user",
			"body": "Test body post (updated)"
		}

		response = client.put(f'{self.endpoint}{post.public_id}/', data)

		assert response.status_code == status.HTTP_401_UNAUTHORIZED
	
	def test_delete_anonymous(self, client, post):
		response = client.delete(f'{self.endpoint}{post.public_id}/')

		assert response.status_code == status.HTTP_401_UNAUTHORIZED