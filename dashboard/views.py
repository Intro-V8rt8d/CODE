from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Video, Document, ResourceSaved, Category
from .forms import SearchForm, VideoForm, DocumentForm
from django.http import FileResponse, Http404
from accounts.models import Profile

def home(request):
    return render(request, "home.html")

def simple(request, title, body):
    return render(request, "simple_page.html", {"title": title, "body": body})

def about(request): 
    return simple(request, "About us", "We provide virtual classroom experiences.")

def services(request): 
    return simple(request, "Services", "Live classes, assignments, uploads and resources.")

def contact(request): 
    return simple(request, "Contact", "Email: hello@example.com")


@login_required
def dashboard(request):
    form = SearchForm(request.GET or None)
    q = ""
    videos = Video.objects.order_by("-created_at")[:6]
    docs = Document.objects.order_by("-created_at")[:6]
    if form.is_valid():
        q = form.cleaned_data.get("q", "")
        if q:
            videos = Video.objects.filter(title__icontains=q) | Video.objects.filter(
                uploader__username__icontains=q
            )
            docs = Document.objects.filter(title__icontains=q) | Document.objects.filter(
                uploader__username__icontains=q
            )
            if not videos.exists():
                messages.info(request, "No matching videos found.")
            if not docs.exists():
                messages.info(request, "No matching documents found.")
    context = {"form": form, "videos": videos, "docs": docs}
    return render(request, "dashboard/dashboard.html", context)


@login_required
def upload(request):
    # ✅ Guarantee profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)
    if profile.role != "tutor":
        messages.error(request, "Only tutors can upload.")
        return redirect("dashboard:dashboard")

    vform = VideoForm(request.POST or None)
    dform = DocumentForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if "save_video" in request.POST and vform.is_valid():
            v = vform.save(commit=False)
            v.uploader = request.user
            v.save()
            messages.success(request, "Video saved.")
            return redirect("dashboard:upload")
        if "save_doc" in request.POST and dform.is_valid():
            d = dform.save(commit=False)
            d.uploader = request.user
            d.save()
            messages.success(request, "Document uploaded.")
            return redirect("dashboard:upload")

    return render(request, "dashboard/upload.html", {"vform": vform, "dform": dform})


@login_required
def download_doc(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    # mark saved resource
    ResourceSaved.objects.get_or_create(user=request.user, document=doc)
    if not doc.file:
        raise Http404("No file")
    return FileResponse(
        doc.file.open("rb"),
        as_attachment=True,
        filename=doc.file.name.split("/")[-1],
    )


@login_required
def resources(request):
    saved = (
        ResourceSaved.objects.filter(user=request.user)
        .select_related("document")
        .order_by("-saved_at")
    )
    return render(request, "dashboard/resources.html", {"saved": saved})
