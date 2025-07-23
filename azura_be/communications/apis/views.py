from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from azura_be.communications.apis.serializers import CommunicationMessageSerializer
from azura_be.communications.apis.serializers import ThreadSerializer
from azura_be.communications.models import CommunicationMessage
from azura_be.communications.models import Thread
from azura_be.communications.models import ThreadUser
from azura_be.users.apis.serializers import UserRelatedSerializer
from azura_be.users.models import User


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    http_method_names = ["get", "patch", "post", "delete"]
    global_params_optional = True

    def get_queryset(self):
        self.queryset = self.queryset.filter(
            Q(created_by=self.request.user) | Q(thread_users__user=self.request.user)
        )
        return super().get_queryset()

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    @extend_schema(responses=UserRelatedSerializer(many=True))
    @action(detail=True, methods=["GET"])
    def users(self, request, *args, **kwargs):
        thread = self.get_object()
        users = User.objects.filter(user_threads__thread=thread)
        return Response(UserRelatedSerializer(users, many=True).data)

    @extend_schema(responses=ThreadSerializer, request=None)
    @action(detail=True, methods=["PATCH"], url_path="add-user/(?P<user_id>[^/.]+)")
    def add_user(self, request, *args, **kwargs):
        thread = self.get_object()
        user = User.objects.filter(id=kwargs.get("user_id")).first()
        if user is None:
            return Response({"message": "User not found", "extra": None}, status=404)
        if ThreadUser.objects.filter(thread=thread, user=user).exists():
            return Response(
                {
                    "message": "This user is already exists in this thread",
                    "extra": None,
                },
                status=400,
            )
        ThreadUser.objects.create(user=user, thread=thread, added_by=request.user)
        return Response(ThreadSerializer(thread).data)


class CommunicationMessageViewSet(
    mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = CommunicationMessage.objects.all()
    serializer_class = CommunicationMessageSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user)
        return super().get_queryset()

    @extend_schema(responses=CommunicationMessageSerializer, request=None)
    @action(detail=True, methods=["PATCH"], url_path="mark-read")
    def mark_read(self, request, *args, **kwargs):
        communication_message = self.get_object()
        communication_message.read = True
        communication_message.save()
        return Response(CommunicationMessageSerializer(communication_message).data)
