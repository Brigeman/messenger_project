from rest_framework import viewsets
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Chat, Message, Profile
from .serializers import ChatSerializer, MessageSerializer, UserSerializer
from django.shortcuts import render, redirect
from .forms import SignUpForm, UserEditForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "chat/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        chat = serializer.save()
        chat.members.add(self.request.user)
        chat.save()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@login_required
def index(request, room_name=None):
    user_profile = Profile.objects.get(user=request.user)
    return render(
        request, "chat/index.html", {"profile": user_profile, "room_name": room_name}
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserEditForm(instance=request.user.profile)
    return render(request, "chat/edit_profile.html", {"form": form})


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "chat/user_list.html", {"users": users})
