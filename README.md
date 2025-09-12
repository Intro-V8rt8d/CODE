# VirtClass — Virtual Classroom (Django + Channels)

## Quickstart
```bash
cd virtclass_project
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000

## Notes
- Login supports **username or email**. If neither exists: *"account doesn’t exist"*. If wrong password: *"invalid credentials"*.
- Emails are **not unique**, usernames **must be unique** and contain letters and numbers.
- Tutors can upload YouTube IDs and documents. Students see docs & videos on the dashboard and can download docs which get stored in **Resources**.
- Assignments have a secret **code**; students can find by code. Tutors can add objective questions and students get auto-marked percentages.
- **Live** uses WebRTC with Channels for signaling. Tutor starts a session (gets a room code). Students join by code. Attendance and basic presence logs are recorded.
- Theme toggle: emoji-based light/dark. Online indicator shows as a green dot.
- Styling uses **plain CSS** with hover/active transitions.
- For production, switch CHANNEL_LAYERS to Redis and configure static files.
```python
CHANNEL_LAYERS = { "default": { "BACKEND": "channels_redis.core.RedisChannelLayer", "CONFIG": { "hosts": [("127.0.0.1", 6379)] } } }
```
