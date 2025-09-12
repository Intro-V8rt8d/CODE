from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Assignment, Submission, ObjectiveQuestion, Option
from .forms import AssignmentForm, ObjectiveForm

@login_required
def list_assignments(request):
    q = request.GET.get("code","").strip().upper()
    found = None
    if q:
        try:
            found = Assignment.objects.get(code=q)
        except Assignment.DoesNotExist:
            messages.error(request, "Assignment not found.")
    owned = Assignment.objects.filter(creator=request.user).order_by("-created_at") if request.user.profile.role == "tutor" else None
    return render(request, "assignments/list.html", {"found": found, "owned": owned})

@login_required
def create_assignment(request):
    if request.user.profile.role != "tutor":
        messages.error(request, "Only tutors can create assignments.")
        return redirect("assignments:list")
    form = AssignmentForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        a = form.save(commit=False)
        a.creator = request.user
        a.save()
        messages.success(request, f"Assignment created with code {a.code}")
        return redirect("assignments:detail", code=a.code)
    return render(request, "assignments/create.html", {"form": form})

@login_required
def add_objective(request, code):
    a = get_object_or_404(Assignment, code=code)
    if request.user != a.creator:
        messages.error(request, "Only the creator can modify this assignment.")
        return redirect("assignments:detail", code=code)
    form = ObjectiveForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        q = ObjectiveQuestion.objects.create(assignment=a, text=form.cleaned_data["question"])
        opts = [
            ("A", form.cleaned_data["option_a"]),
            ("B", form.cleaned_data["option_b"]),
            ("C", form.cleaned_data.get("option_c")),
            ("D", form.cleaned_data.get("option_d")),
        ]
        for label, text in opts:
            if text:
                Option.objects.create(question=q, text=text, is_correct=(label == form.cleaned_data["correct"]))
        messages.success(request, "Objective question added.")
        return redirect("assignments:detail", code=code)
    return render(request, "assignments/add_objective.html", {"form": form, "assignment": a})

@login_required
def detail(request, code):
    a = get_object_or_404(Assignment, code=code)
    sub = Submission.objects.filter(assignment=a, student=request.user).first()
    return render(request, "assignments/detail.html", {"a": a, "sub": sub})

@login_required
def submit(request, code):
    a = get_object_or_404(Assignment, code=code)
    if not a.submit_here:
        messages.error(request, "This assignment is not to be submitted here.")
        return redirect("assignments:detail", code=code)
    if request.method == "POST":
        file = request.FILES.get("answer_file")
        Submission.objects.update_or_create(assignment=a, student=request.user, defaults={"answer_file": file})
        messages.success(request, "Submitted.")
        return redirect("assignments:detail", code=code)
    return render(request, "assignments/submit.html", {"a": a})

@login_required
def answer_objective(request, code):
    a = get_object_or_404(Assignment, code=code)
    if request.method == "POST":
        total = a.questions.count() or 1
        correct = 0
        for q in a.questions.all():
            chosen = request.POST.get(f"q{q.id}")
            if chosen:
                opt = q.options.filter(id=int(chosen)).first()
                if opt and opt.is_correct:
                    correct += 1
        percent = int(100 * correct / total)
        sub, _ = Submission.objects.get_or_create(assignment=a, student=request.user)
        sub.score = percent
        sub.save()
        messages.success(request, f"Your score: {percent}")
        return redirect("assignments:detail", code=code)
    return render(request, "assignments/answer_objective.html", {"a": a})
