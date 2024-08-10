import pytest

from fixtures.user import user
from posts.models import Post


@pytest.fixture
def post(db, user) -> Post:
	return Post.objects.create(author=user, body="Test Post Body")