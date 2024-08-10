import pytest

from fixtures.user import user
from posts.models import Post


@pytest.mark.django_db
def test_create_post(user):
	post = Post.objects.create(author=user, body="Test Body Post")

	assert post.body == "Test Body Post"
	assert post.author == user