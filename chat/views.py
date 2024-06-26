from rest_framework import viewsets
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Chat, Message, Profile
from .serializers import ChatSerializer, MessageSerializer, UserSerializer
from django.shortcuts import render, redirect
from .forms import (
    UserEditForm,
    UsernameAuthenticationForm,
    GroupChatForm,
    AddUserToGroupForm,
)
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)


def signup(request):
    error_message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                logger.info(f"Signup attempt with existing username: {username}")
                error_message = "Username already exists."
            else:
                user = User.objects.create(username=username)
                logger.info(f"New user created: {username}")
                # check profile
                if not Profile.objects.filter(user=user).exists():
                    Profile.objects.create(user=user)
                    logger.info(f"Profile created for user: {username}")
                login(request, user)
                logger.info(f"User logged in: {username}")
                return redirect("index")
    return render(request, "chat/signup.html", {"error_message": error_message})


# TODO log
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        chat = serializer.save()
        chat.members.add(self.request.user)
        chat.save()
        logger.info(f"New chat created by user {self.request.user}: {chat.id}")


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(
            f"New message created by user {self.request.user}: {serializer.instance.id}"
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def login_view(request):
    if request.method == "POST":
        form = UsernameAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user = User.objects.get(username=username)
            login(request, user)
            logger.info(f"User logged in: {username}")
            return redirect("index")
    else:
        form = UsernameAuthenticationForm()
    return render(request, "chat/login.html", {"form": form})


@login_required
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    logger.info(f"Rendering index for user: {request.user.username}")
    return render(request, "chat/index.html", {"profile": user_profile})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            logger.info(f"Profile updated for user: {request.user.username}")
            return redirect("index")
    else:
        form = UserEditForm(instance=request.user.profile)
    return render(request, "chat/edit_profile.html", {"form": form})


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    logger.info(f"Rendering user list for user: {request.user.username}")
    return render(request, "chat/user_list.html", {"users": users})


@login_required
def private_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    logger.info(
        f"Rendering private chat between user: {request.user.username} and user: {other_user.username}"
    )
    return render(request, "chat/private_chat.html", {"other_user": other_user})


@login_required
def create_group_chat(request):
    if request.method == "POST":
        form = GroupChatForm(request.POST)
        if form.is_valid():
            group_chat = form.save(commit=False)
            group_chat.is_group = True
            group_chat.save()
            group_chat.members.add(request.user)
            logger.info(f"Group chat created by user: {request.user.username}")
            return redirect("add_users_to_group", group_chat_id=group_chat.id)
        else:
            logger.error(f"Error creating group chat: {form.errors}")
    else:
        form = GroupChatForm()
    return render(request, "chat/create_group_chat.html", {"form": form})


@login_required
def add_users_to_group(request, group_chat_id):
    group_chat = Chat.objects.get(id=group_chat_id)
    if request.method == "POST":
        form = AddUserToGroupForm(request.POST)
        if form.is_valid():
            users = form.cleaned_data["users"]
            for user in users:
                group_chat.members.add(user)
            logger.info(
                f"Users added to group chat {group_chat.name} by {request.user.username}"
            )
            return redirect("group_chat", room_name=group_chat.name)
    else:
        form = AddUserToGroupForm()
    return render(
        request,
        "chat/add_users_to_group.html",
        {"form": form, "group_chat": group_chat},
    )


@login_required
def group_chat_view(request, room_name):
    user_profile = Profile.objects.get(user=request.user)
    logger.info(
        f"Rendering group chat for user: {request.user.username} in room: {room_name}"
    )
    return render(
        request,
        "chat/group_chat.html",
        {"profile": user_profile, "room_name": room_name},
    )
