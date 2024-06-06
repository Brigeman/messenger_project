from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChatViewSet,
    MessageViewSet,
    UserViewSet,
    signup,
    edit_profile,
    user_list,
    index,
)

router = DefaultRouter()
router.register(r"chats", ChatViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("user_list/", user_list, name="user_list"),
    path("api/", include(router.urls)),
    path("<str:room_name>/", index, name="chat_room"),
    path("", index, name="index"),
]
