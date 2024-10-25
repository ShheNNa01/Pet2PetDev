import json
from typing import Any, Optional
import redis.asyncio as redis
from shared.config.settings import settings

class NotificationEventBroker:
    def __init__(self):
        self.redis = None
        self.pubsub = None

    async def connect(self):
        if not self.redis:
            self.redis = redis.Redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )

    async def publish_event(self, channel: str, event_data: dict[str, Any]):
        """Publica un evento en un canal específico"""
        await self.connect()
        await self.redis.publish(channel, json.dumps(event_data))

    async def subscribe(self, channel: str):
        """Suscribe a un canal específico"""
        await self.connect()
        if not self.pubsub:
            self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe(channel)
        return self.pubsub

    async def close(self):
        """Cierra las conexiones"""
        if self.pubsub:
            await self.pubsub.close()
        if self.redis:
            await self.redis.close()

event_broker = NotificationEventBroker()