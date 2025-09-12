from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm
from .models import Profile

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ue = form.cleaned_data["username_or_email"]
        pwd = form.cleaned_data["password"]
        user = None
        # Try username
        user = authenticate(request, username=ue, password=pwd)
        if not user:
            # Try email (multiple users may share email -> pick first exact match)
            qs = User.objects.filter(email__iexact=ue)
            for u in qs:
                user = authenticate(request, username=u.username, password=pwd)
                if user:
                    break
        if user:
            login(request, user)
            return redirect("dashboard:dashboard")
        else:
            # differentiate invalid credentials vs account doesn't exist
            if not User.objects.filter(username__iexact=ue).exists() and not User.objects.filter(email__iexact=ue).exists():
                messages.error(request, "account doesn’t exist")
            else:
                messages.error(request, "invalid credentials")
            return redirect("accounts:login")
    return render(request, "accounts/login.html", {"form": form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            # Update the auto-created profile
            profile = user.profile
            profile.full_name = form.cleaned_data["full_name"]
            profile.role = form.cleaned_data["role"]
            profile.save()

            
            login(request, user)
            return redirect("dashboard:dashboard")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("home")
