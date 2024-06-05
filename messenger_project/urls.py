from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chat.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/<str:room_name>/", index, name="chat_room"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", index, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
