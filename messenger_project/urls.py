from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chat.views import index, login_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls")),
    # path("accounts/login/", login_view, name="login"),
    path("", index, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
