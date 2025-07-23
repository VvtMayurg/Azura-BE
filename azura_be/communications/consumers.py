from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Q

from azura_be.communications.apis.serializers import ThreadMessageSerializer
from azura_be.communications.models import Thread
from azura_be.communications.models import ThreadMessage


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.send_json({"type": "connection", "message": "Connection Failed"})
            return
        await self.accept()

        self.group_name = f"{self.user.keycloak_id!s}__notification"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.send_json({"type": "connection", "message": "Connection Success"})

    async def send_notification(self, event):
        await self.send_json(event["message"])

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        return await super().disconnect(code)


class ThreadChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        thread_id = self.scope["url_route"]["kwargs"]["thread_id"]
        if not self.user.is_authenticated:
            await self.send_json({"type": "connection", "message": "Connection Failed"})
            return
        await self.accept()
        await self.get_thread()

        self.group_name = f"{thread_id}__thread"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.send_json({"type": "connection", "message": "Connection Success"})
        await self.send_json({"type": "last_messages", "last_messages": self.messages})

    @sync_to_async
    def get_thread(self):
        thread_id = self.scope["url_route"]["kwargs"]["thread_id"]
        self.thread = Thread.objects.filter(Q(created_by=self.user) | Q(thread_users__user=self.user)).get(id=thread_id)
        self.messages = ThreadMessageSerializer(
            ThreadMessage.objects.select_related("user").prefetch_related("thread_message_attachments").filter(thread=self.thread)[:25],
            many=True,
        ).data

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        return await super().disconnect(code)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if not text_data and not bytes_data:
            return await self.send_json({"type": "receive", "message": "No Data Received"})
        if bytes_data:
            return await self.send_json({"type": "receive", "message": "Bytes Data Received"})

        data = await self.decode_json(text_data)
        if data.get("type") == "new_message":
            message = data.get("message")
            return await self.send_json({"type": "new_message", "message": ThreadMessageSerializer(await self.save_new_message(message)).data})
        return await self.send_json({"type": "receive", "message": "Text Data Received"})

    @sync_to_async
    def save_new_message(self, content):
        return ThreadMessage.objects.create(thread=self.thread, user=self.user, content=content)
