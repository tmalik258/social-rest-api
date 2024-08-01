from rest_framework import (permissions, status)
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import (TokenError, InvalidToken)


class RefreshViewSet(ViewSet, TokenRefreshView):
	http_method_names = ['post']
	permission_classes = [permissions.AllowAny]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		try:
			serializer.is_valid(raise_exception=True)
		except TokenError as e:
			raise InvalidToken(e.args[0])

		return Response(serializer.validated_data, status=status.HTTP_200_OK)