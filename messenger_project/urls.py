from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chat.views import index
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="chat/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", index, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
