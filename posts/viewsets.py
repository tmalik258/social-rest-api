from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from abstract.viewsets import AbstractViewSet
from posts.models import Post
from auth.permissions import UserPermission
from posts.serializers import PostSerializer


class PostViewSet(AbstractViewSet):
    permission_classes = [UserPermission]
    serializer_class = PostSerializer
    http_method_names = ["post", "get", "put", "delete"]
    queryset = Post.objects.all()

    @action(methods=["post"], detail=True)
    def toggle_like(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        # Check if the user has already liked the post
        if user.has_liked(instance):
            user.unlike(instance)  # Remove like
            action = "unliked"
        else:
            user.like(instance)  # Add like
            action = "liked"

        serializer = self.serializer_class(instance, context={"request": request})
        return Response(
            {"action": action, "post": serializer.data}, status=status.HTTP_200_OK
        )

    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs["pk"])

        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if not instance.edited:
            serializer.validated_data["edited"] = True

        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
