import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import Chat

User = get_user_model()
logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Проверяем, является ли комната групповой
        self.is_group = await self.is_group_chat()

        logger.debug(
            f"Connecting to room: {self.room_group_name} (Group: {self.is_group})"
        )

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.debug(f"WebSocket accepted for room: {self.room_group_name}")

    async def disconnect(self, close_code):
        logger.debug(
            f"Disconnecting from room: {self.room_group_name}, code: {close_code}"
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        logger.debug(f"Message received: {message}")
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]
        logger.debug(f"Sending message: {message}")
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def is_group_chat(self):
        try:
            chat = Chat.objects.get(name=self.room_name)
            return chat.is_group
        except Chat.DoesNotExist:
            return False


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = int(self.scope["url_route"]["kwargs"]["user_id"])
        self.room_name = f'private_chat_{min(self.user_id, self.scope["user"].id)}_{max(self.user_id, self.scope["user"].id)}'
        self.room_group_name = f"chat_{self.room_name}"

        logger.debug(f"Connecting to private chat room: {self.room_group_name}")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.debug(
            f"WebSocket accepted for private chat room: {self.room_group_name}"
        )

    async def disconnect(self, close_code):
        logger.debug(
            f"Disconnecting from private chat room: {self.room_group_name}, code: {close_code}"
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        logger.debug(
            f"Message received in private chat: {message} from user {self.scope['user'].username}"
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.scope["user"].username,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        logger.debug(f"Sending message in private chat: {message} from {sender}")
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))
