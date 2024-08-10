import pytest

from comments.models import Comment
from fixtures.user import user
from fixtures.post import post

@pytest.fixture
def comment(db, user, post):
	return Comment.objects.create(author=user, post=post, body='Test Comment Body')