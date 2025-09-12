from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.ModelForm):
    full_name = forms.CharField()
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_username(self):
        u = self.cleaned_data.get("username")
        if not any(ch.isalpha() for ch in u) or not any(ch.isdigit() for ch in u):
            raise forms.ValidationError("Username must include letters and numbers.")
        if User.objects.filter(username__iexact=u).exists():
            raise forms.ValidationError("username already taken")
        return u

    def clean(self):
        cd = super().clean()
        if cd.get("password") != cd.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match")
        return cd
