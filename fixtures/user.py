import pytest

from django.contrib.auth import get_user_model


data_user = {
	"username": "test_user",
	"email": "test@gmail.com",
	"first_name": "Test",
	"last_name": "User",
	"password": "test_password"
}


@pytest.fixture
def user(db) -> get_user_model:
	return get_user_model().objects.create_user(**data_user)