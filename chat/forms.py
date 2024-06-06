from django import forms
from .models import Profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio")
