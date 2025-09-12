from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import LiveSession, Participant

@login_required
def start_live(request):
    if request.user.profile.role != "tutor":
        # students get join page with room code search
        return render(request, "live/join.html")
    if request.method == "POST":
        # end all previous lives
        LiveSession.objects.filter(
            tutor=request.user, is_active=True
        ).update(is_active=False, ended_at=timezone.now())
        s = LiveSession.objects.create(tutor=request.user, is_active=True)
        messages.success(request, f"Live started. Share room code {s.room}")
        return redirect("live:room", room=s.room)
    # show button to start or join
    return render(request, "live/start.html")

@login_required
def join_live(request):
    room = request.GET.get("room", "").strip().upper()
    try:
        s = LiveSession.objects.get(room=room, is_active=True)
    except LiveSession.DoesNotExist:
        messages.error(request, "Live room not found")
        return redirect("live:start")
    return redirect("live:room", room=s.room)

@login_required
def room(request, room):
    try:
        s = LiveSession.objects.get(room=room)
    except LiveSession.DoesNotExist:
        messages.error(request, "Live class ended")
        return redirect("live:start")

    if not s.is_active:
        messages.error(request, "Live class ended")
        return redirect("live:start")

    # ✅ pass is_tutor to avoid inline template logic
    is_tutor = (request.user == s.tutor)

    return render(
        request,
        "live/room.html",
        {
            "room": room,
            "session": s,
            "is_tutor": is_tutor,
        },
    )

@login_required
def end_live(request, room):
    s = get_object_or_404(LiveSession, room=room, tutor=request.user)
    s.is_active = False
    s.ended_at = timezone.now()
    s.save()
    messages.success(request, "Live ended.")
    return redirect("live:start")

@login_required
def attendance(request, room):
    s = get_object_or_404(LiveSession, room=room)
    parts = s.participants.all().order_by("-joined_at")
    return render(request, "live/attendance.html", {"session": s, "parts": parts})
