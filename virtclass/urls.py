from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from dashboard.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path("assignments/", include(("assignments.urls", "assignments"), namespace="assignments")),
    path("live/", include(("liveapp.urls", "liveapp"), namespace="live")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
