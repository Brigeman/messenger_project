from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UsernameAuthenticationForm(forms.Form):
    username = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Invalid username")
        return username


class UserEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio")
