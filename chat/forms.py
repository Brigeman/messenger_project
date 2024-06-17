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
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Group Chat Name"}
            )
        }


class AddUserToGroupForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple
    )
