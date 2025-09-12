import json, datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import LiveSession, Participant

@database_sync_to_async
def get_session(room):
    try:
        return LiveSession.objects.get(room=room, is_active=True)
    except LiveSession.DoesNotExist:
        return None

@database_sync_to_async
def add_participant(session, user_id):
    user = User.objects.get(id=user_id)
    p, created = Participant.objects.get_or_create(session=session, user=user)
    if p.kicked:
        return None
    if p.left_at:
        p.left_at = None
        p.save()
    return p

@database_sync_to_async
def mark_left(session, user_id):
    try:
        p = Participant.objects.get(session=session, user_id=user_id)
        p.left_at = datetime.datetime.utcnow()
        p.save()
    except Participant.DoesNotExist:
        pass

@database_sync_to_async
def count_participants(session):
    return session.participants.filter(left_at__isnull=True, kicked=False).count()

@database_sync_to_async
def kick_user(session, user_id):
    try:
        p = Participant.objects.get(session=session, user_id=user_id)
        p.kicked = True
        p.left_at = datetime.datetime.utcnow()
        p.save()
        return True
    except Participant.DoesNotExist:
        return False

class LiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = self.scope['url_route']['kwargs']['room']
        self.session = await get_session(self.room)
        if not self.session:
            await self.close()
            return
        self.group = f"live_{self.room}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        if self.scope["user"].is_authenticated:
            p = await add_participant(self.session, self.scope["user"].id)
            if p is None:
                await self.close()
                return
            await self.channel_layer.group_send(self.group, {{
                "type":"presence.join",
                "full_name": self.scope["user"].profile.full_name,
                "user_id": self.scope["user"].id,
            }})
        await self.accept()

    async def disconnect(self, code):
        if getattr(self, "session", None) and self.scope["user"].is_authenticated:
            await mark_left(self.session, self.scope["user"].id)
            await self.channel_layer.group_send(self.group, {{
                "type":"presence.leave",
                "full_name": self.scope["user"].profile.full_name,
                "user_id": self.scope["user"].id,
            }})
        if getattr(self, "group", None):
            await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data or "{}")
        # Signaling for WebRTC passthrough
        if data.get("action") in ["offer","answer","candidate"]:
            await self.channel_layer.group_send(self.group, {{
                "type":"signal",
                "sender": self.scope["user"].id if self.scope["user"].is_authenticated else None,
                "payload": data,
            }})
        elif data.get("action") == "count":
            c = await count_participants(self.session)
            await self.send(text_data=json.dumps({{"type":"count","count":c}}))
        elif data.get("action") == "kick" and self.scope["user"].id == self.session.tutor_id:
            uid = int(data.get("user_id"))
            if await kick_user(self.session, uid):
                await self.channel_layer.group_send(self.group, {{
                    "type":"presence.kicked",
                    "user_id": uid,
                }})

    async def signal(self, event):
        await self.send(text_data=json.dumps({{"type":"signal","from":event.get("sender"),"payload":event.get("payload")}}))

    async def presence_join(self, event):
        await self.send(text_data=json.dumps({{"type":"presence","event":"join","full_name":event["full_name"],"user_id":event["user_id"]}}))

    async def presence_leave(self, event):
        await self.send(text_data=json.dumps({{"type":"presence","event":"leave","full_name":event["full_name"],"user_id":event["user_id"]}}))

    async def presence_kicked(self, event):
        await self.send(text_data=json.dumps({{"type":"presence","event":"kicked","user_id":event["user_id"]}}))
