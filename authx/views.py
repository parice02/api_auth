from rest_framework.response import Response
from rest_framework import viewsets, status, decorators


from .permissions import UserReadWritePermission, AdminPermission
from .serializers import (
    ExtendedUserSerializer,
    SecureUserSerializer,
    RestrictedUserSerializer,
)
from .models import CustomUser

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ("list", "retrieve"):
            serializer_class = SecureUserSerializer
        else:
            serializer_class = ExtendedUserSerializer
        return serializer_class

    def get_permissions(self):
        if self.action in ("list",):
            permission_classes = [AdminPermission]
        else:
            permission_classes = [UserReadWritePermission]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            instance.is_staff = False
            instance.is_superuser = False
            instance.is_active = True
            instance.save()
        response = {"id": instance.id, "username": instance.username}
        return Response(response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        user.is_active = False
        user.save()
        return Response(
            {"detail": f"user '{user.phone}' was successfully deleted"},
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=["GET"], detail=False)
    def info(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = RestrictedUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(methods=["GET"], detail=True)
    def activate(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        user.is_active = True
        serializer = RestrictedUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
