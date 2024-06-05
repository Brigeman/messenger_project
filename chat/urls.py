from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChatViewSet,
    MessageViewSet,
    UserViewSet,
    signup,
    login_view,
    index,
    edit_profile,
    user_list,
)

router = DefaultRouter()
router.register(r"chats", ChatViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("", index, name="home"),
    path("chat/<str:room_name>/", index, name="chat_room"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("user_list/", user_list, name="user_list"),
    path("api/", include(router.urls)),
]
