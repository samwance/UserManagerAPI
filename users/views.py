from rest_framework import viewsets, status
from rest_framework.response import Response

from .repositories import get_repository
from .serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    repository = get_repository()

    def list(self, request):
        users = self.repository.list()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        full_name = request.data.get("full_name")
        user = self.repository.create(full_name)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        user = self.repository.get(int(pk))
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        full_name = request.data.get("full_name")
        try:
            user = self.repository.update(int(pk), full_name)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            self.repository.delete(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
