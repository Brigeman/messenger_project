from django import forms
from django.contrib.auth.models import User
from .models import Profile, Chat


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


class GroupChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Chat.objects.filter(name=name).exists():
            raise forms.ValidationError("Chat with this name already exists.")
        return name


class AddUserToGroupForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple
    )
